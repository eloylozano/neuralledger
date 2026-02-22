import os
import shutil
import re
import uuid
import time
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import OperationalError
from typing import Optional

# Importaciones de tus archivos
from database import engine, get_db
import models
import schemas
from utils.processor import process_pdf_to_json

# --- LÓGICA DE INICIALIZACIÓN ROBUSTA ---
def init_db():
    """Intenta crear las tablas con reintentos si la DB no está lista"""
    retries = 15
    while retries > 0:
        try:
            print("Intentando conectar a la base de datos...")
            models.Base.metadata.create_all(bind=engine)
            print("¡Tablas creadas/verificadas con éxito!")
            return
        except OperationalError as e:
            retries -= 1
            print(f"Base de datos no lista (quedan {retries} intentos). Esperando 3s...")
            time.sleep(3)
    print("Error crítico: No se pudo conectar a la base de datos.")

# Llamamos a la creación de tablas con seguridad
init_db()

app = FastAPI(title="NeuralLedger API")

# --- CONFIGURACIÓN CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "storage"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/process-invoice/")
async def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Generamos un nombre único: ej. "a1b2-c3d4...pdf"
    file_id = str(uuid.uuid4())
    temp_filename = f"{file_id}.pdf"
    file_path = os.path.join(UPLOAD_DIR, temp_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        
        extracted_data = await process_pdf_to_json(content)
        
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
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-invoice/")
async def save_invoice(data: schemas.InvoiceResponse, db: Session = Depends(get_db)):
    # 1. Manejo de Proveedor
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
        if data.ia_notes:
            db_supplier.ia_notes = data.ia_notes
            db.add(db_supplier)

    # 2. Carpeta de archivos
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', data.supplier_name)
    folder_name = f"{clean_name}_{data.supplier_cif}"
    supplier_dir = os.path.join(UPLOAD_DIR, folder_name)
    
    if not os.path.exists(supplier_dir):
        os.makedirs(supplier_dir)

    # 3. Nombre final PDF
    clean_inv_num = data.invoice_num.replace("/", "-").replace(" ", "_")
    final_filename = f"Factura_{clean_inv_num}.pdf"
    final_pdf_path = os.path.join(supplier_dir, final_filename)

    # 4. Movimiento del archivo usando el nombre único que viene del Front
    temp_path = os.path.join(UPLOAD_DIR, data.temp_file) 
    
    if os.path.exists(temp_path):
        shutil.move(temp_path, final_pdf_path)
    elif os.path.exists(final_pdf_path):
        pass # Ya estaba allí
    else:
        raise HTTPException(status_code=404, detail="Archivo PDF no encontrado.")
    
    # 5. Guardar Factura
    new_invoice = models.Invoice(
        invoice_num=data.invoice_num,
        date_str=data.date,
        taxable_base=data.taxable_base,
        vat=data.vat,
        discount=data.discount,
        total=data.total,
        supplier_id=db_supplier.id,
        pdf_path=final_pdf_path 
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    # 6. Items (Lineas de factura)
    for item in data.items:
        item_data = item.model_dump()
        
        # Lógica de seguridad para impuestos
        tax_value = item_data.get('tax') 
        if tax_value is None:
            tax_value = item_data.get('ia_notes', 0.0)

        db_item = models.InvoiceLine(
            position=item_data.get('position'),
            description=item_data.get('description'),
            quantity=item_data.get('quantity'),
            price=item_data.get('price'),
            tax=float(tax_value) if tax_value is not None else 0.0, 
            discount=item_data.get('discount', 0.0),
            total_item=item_data.get('total_item'),
            invoice_id=new_invoice.id
        )
        db.add(db_item)
    
    db.commit()
    
    return {
        "message": "Factura guardada correctamente",
        "pdf_location": final_pdf_path
    }

@app.get("/invoices/")
async def list_invoices(db: Session = Depends(get_db)):
    return db.query(models.Invoice).options(joinedload(models.Invoice.supplier)).all()