import os
import shutil
import re
import uuid
import time
import logging
import fitz 
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import OperationalError
from typing import Optional, List
from sqlalchemy import func

# Importaciones locales
from database import engine, get_db
import models
import schemas
from utils.processor import process_pdf_to_json

# 1. CONFIGURACIÓN INICIAL
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_DIR = "storage"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 2. INICIALIZACIÓN DE LA APP
app = FastAPI(title="NeuralLedger API")

# 3. MIDDLEWARES Y ESTÁTICOS (Deben ir después de instanciar FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir la carpeta de almacenamiento para que el PDF se vea en el navegador
app.mount("/storage", StaticFiles(directory=UPLOAD_DIR), name="storage")

def init_db():
    retries = 15
    while retries > 0:
        try:
            models.Base.metadata.create_all(bind=engine)
            logger.info("Base de datos conectada con éxito")
            return
        except OperationalError:
            retries -= 1
            logger.warning(f"Error conectando a DB, reintentando... ({retries} intentos restantes)")
            time.sleep(3)

init_db()

# 4. ENDPOINTS

@app.post("/process-invoice/")
async def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_id = str(uuid.uuid4())
    temp_filename = f"{file_id}.pdf"
    file_path = os.path.join(UPLOAD_DIR, temp_filename)
    
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 1. Extracción de texto única y rápida
        doc = fitz.open(stream=content, filetype="pdf")
        full_text = ""
        for page in doc:
            blocks = page.get_text("blocks")
            blocks.sort(key=lambda b: (b[1], b[0])) # Orden natural de lectura
            for b in blocks:
                full_text += f"{b[4]}\n"
        doc.close()

        # 2. Búsqueda de CIF con Normalización (Memoria)
        historical_context = ""
        cif_pattern = r'([ABCDEFGHJKLMNPQSVW][\s\.\-]?\d{8})|(\d{8}[\s\.\-]?[TRWAGMYFPDXBNJZSQVHLCKE])'
        cif_match = re.search(cif_pattern, full_text.upper())

        if cif_match:
            raw_cif = cif_match.group(0)
            clean_cif = re.sub(r'[^A-Z0-9]', '', raw_cif)
            
            db_supplier = db.query(models.Supplier).filter(models.Supplier.cif == clean_cif).first()
            if db_supplier and db_supplier.ia_notes:
                historical_context = db_supplier.ia_notes
                logger.info(f"Memoria encontrada para {clean_cif}: {historical_context}")

        # 3. Procesar con IA (pasando el contexto histórico si existe)
        extracted_data = await process_pdf_to_json(full_text, context=historical_context)
        extracted_data.temp_file = temp_filename
        
        # Verificar proveedor para el Front (si ya lo conocemos)
        db_supplier = db.query(models.Supplier).filter(
            models.Supplier.cif == extracted_data.supplier_cif
        ).first()
        
        return {
            "extracted": extracted_data,
            "temp_file": temp_filename, 
            "db_supplier": db_supplier,
            "is_new_supplier": db_supplier is None
        }

    except Exception as e:
        if os.path.exists(file_path): os.remove(file_path)
        logger.error(f"Error en el procesamiento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en IA: {repr(e)}")

@app.post("/save-invoice/")
async def save_invoice(data: schemas.InvoiceResponse, db: Session = Depends(get_db)):
    # 1. Gestión del Proveedor (Crear o Actualizar Notas)
    db_supplier = db.query(models.Supplier).filter(models.Supplier.cif == data.supplier_cif).first()
    
    if not db_supplier:
        db_supplier = models.Supplier(
            name=data.supplier_name,
            cif=data.supplier_cif,
            address="Verificado en revisión",
            ia_notes=data.ia_notes
        )
        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)
    else:
        # Actualizamos la memoria del proveedor con las nuevas notas de la IA
        if data.ia_notes:
            db_supplier.ia_notes = data.ia_notes
            db.add(db_supplier)

    # 2. Organización de carpetas por proveedor
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', data.supplier_name)
    folder_name = f"{clean_name}_{data.supplier_cif}"
    supplier_dir = os.path.join(UPLOAD_DIR, folder_name)
    if not os.path.exists(supplier_dir): 
        os.makedirs(supplier_dir)

    # 3. Mover archivo de temp a carpeta final
    clean_inv_num = data.invoice_num.replace("/", "-").replace(" ", "_")
    final_filename = f"Factura_{clean_inv_num}.pdf"
    
    # Path físico para el SO
    absolute_pdf_path = os.path.join(supplier_dir, final_filename)
    # Path relativo para la URL del navegador (Frontend)
    relative_pdf_path = f"storage/{folder_name}/{final_filename}"

    temp_path = os.path.join(UPLOAD_DIR, data.temp_file) 
    if os.path.exists(temp_path):
        shutil.move(temp_path, absolute_pdf_path)
    
    # 4. Crear la Factura en DB
    new_invoice = models.Invoice(
        invoice_num=data.invoice_num,
        date_str=data.date,
        taxable_base=data.taxable_base,
        vat=data.vat,
        discount=data.discount,
        total=data.total,
        supplier_id=db_supplier.id,
        pdf_path=relative_pdf_path 
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    # 5. Guardar Líneas de Detalle
    for item in data.items:
        item_data = item.model_dump()
        tax_val = item_data.get('tax') if item_data.get('tax') is not None else 0.0
        
        db_item = models.InvoiceLine(
            position=item_data.get('position'),
            description=item_data.get('description'),
            quantity=item_data.get('quantity'),
            price=item_data.get('price'),
            tax=float(tax_val), 
            discount=item_data.get('discount', 0.0),
            total_item=item_data.get('total_item'),
            invoice_id=new_invoice.id
        )
        db.add(db_item)
    
    db.commit()
    return {"message": "Factura guardada correctamente", "pdf_url": relative_pdf_path}

@app.get("/invoices/")
async def list_invoices(db: Session = Depends(get_db)):
    # joinedload carga el proveedor en la misma consulta (más rápido)
    return db.query(models.Invoice).options(joinedload(models.Invoice.supplier)).all()

@app.get("/suppliers/", response_model=List[schemas.SupplierResponse]) # Necesitaremos crear este schema
async def list_suppliers(db: Session = Depends(get_db)):
    # Esta consulta trae el proveedor y calcula cuántas facturas tiene y el total gastado
    suppliers = db.query(
        models.Supplier,
        func.count(models.Invoice.id).label("invoice_count"),
        func.sum(models.Invoice.total).label("total_spent")
    ).outerjoin(models.Invoice).group_by(models.Supplier.id).all()
    
    # Formateamos la respuesta
    result = []
    for s, count, total in suppliers:
        s_dict = {
            "id": s.id,
            "name": s.name,
            "cif": s.cif,
            "address": s.address,
            "ia_notes": s.ia_notes,
            "invoice_count": count,
            "total_spent": total or 0.0
        }
        result.append(s_dict)
    return result