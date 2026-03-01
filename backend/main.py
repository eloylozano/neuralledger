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

# Importaciones locales
from database import engine, get_db
import models
import schemas
from utils.processor import process_pdf_to_json

# 1. Inicialización y Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    retries = 15
    while retries > 0:
        try:
            models.Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            retries -= 1
            time.sleep(3)

init_db()

app = FastAPI(title="NeuralLedger API")

# 2. Middlewares y Estáticos (IMPORTANTE: Después de definir 'app')
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

# Servir la carpeta storage para que el Front pueda ver los PDFs
app.mount("/storage", StaticFiles(directory=UPLOAD_DIR), name="storage")

# 3. Endpoints
@app.post("/process-invoice/")
async def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_id = str(uuid.uuid4())
    temp_filename = f"{file_id}.pdf"
    file_path = os.path.join(UPLOAD_DIR, temp_filename)
    
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        doc = fitz.open(stream=content, filetype="pdf")
        full_text = ""
        for page in doc:
            blocks = page.get_text("blocks")
            blocks.sort(key=lambda b: (b[1], b[0]))
            for b in blocks:
                full_text += f"{b[4]}\n"
        doc.close()

        historical_context = ""
        cif_pattern = r'([ABCDEFGHJKLMNPQSVW][\s\.\-]?\d{8})|(\d{8}[\s\.\-]?[TRWAGMYFPDXBNJZSQVHLCKE])'
        cif_match = re.search(cif_pattern, full_text.upper())

        if cif_match:
            raw_cif = cif_match.group(0)
            clean_cif = re.sub(r'[^A-Z0-9]', '', raw_cif)
            db_supplier = db.query(models.Supplier).filter(models.Supplier.cif == clean_cif).first()
            if db_supplier and db_supplier.ia_notes:
                historical_context = db_supplier.ia_notes

        extracted_data = await process_pdf_to_json(full_text, context=historical_context)
        extracted_data.temp_file = temp_filename
        
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
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-invoice/")
async def save_invoice(data: schemas.InvoiceResponse, db: Session = Depends(get_db)):
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

    # Crear ruta final: storage/Nombre_CIF/Factura_Num.pdf
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', data.supplier_name)
    folder_name = f"{clean_name}_{data.supplier_cif}"
    supplier_dir = os.path.join(UPLOAD_DIR, folder_name)
    if not os.path.exists(supplier_dir): os.makedirs(supplier_dir)

    clean_inv_num = data.invoice_num.replace("/", "-").replace(" ", "_")
    final_filename = f"Factura_{clean_inv_num}.pdf"
    
    # Ruta para guardar en DB (usando slashes siempre para URL)
    relative_pdf_path = f"storage/{folder_name}/{final_filename}"
    # Ruta física en disco
    absolute_pdf_path = os.path.join(supplier_dir, final_filename)

    temp_path = os.path.join(UPLOAD_DIR, data.temp_file) 
    if os.path.exists(temp_path):
        shutil.move(temp_path, absolute_pdf_path)
    
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

    for item in data.items:
        db_item = models.InvoiceLine(
            **item.model_dump(),
            invoice_id=new_invoice.id
        )
        db.add(db_item)
    
    db.commit()
    return {"message": "Guardado", "pdf_path": relative_pdf_path}

@app.get("/invoices/")
async def list_invoices(db: Session = Depends(get_db)):
    return db.query(models.Invoice).options(joinedload(models.Invoice.supplier)).all()