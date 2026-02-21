import os
import shutil
from utils.processor import process_pdf_to_json
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

# Importaciones de tus archivos
from database import engine, get_db, SessionLocal
import models
import schemas
from utils.processor import process_pdf_to_json

# Creamos las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="NeuralLedger API")

# Asegurarnos de que la carpeta storage existe
UPLOAD_DIR = "storage"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/process-invoice/", response_model=schemas.InvoiceResponse)
async def upload_invoice(file: UploadFile = File(...)):
    # 1. Guardar el archivo temporalmente para procesarlo
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 2. Leer contenido para la IA
        with open(file_path, "rb") as f:
            content = f.read()
        
        # 3. Llamar al procesador (Ollama + PyMuPDF)
        extracted_data = await process_pdf_to_json(content)
        
        # Devolvemos los datos al frontend para que el usuario los valide
        return extracted_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar: {str(e)}")

@app.post("/save-invoice/")
async def save_invoice(data: schemas.InvoiceResponse, db: Session = Depends(get_db)):
    # 1. Verificar si el proveedor ya existe por CIF
    db_supplier = db.query(models.Supplier).filter(models.Supplier.cif == data.supplier_cif).first()
    
    if not db_supplier:
        # Si no existe, lo creamos
        db_supplier = models.Supplier(
            name=data.supplier_name,
            cif=data.supplier_cif,
            address="Pendiente de verificar" # La IA puede extraer esto luego
        )
        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)

    # 2. Crear la factura vinculada al proveedor
    new_invoice = models.Invoice(
        invoice_num=data.invoice_num,
        date_str=data.date,
        taxable_base=data.taxable_base,
        vat=data.vat,
        discount=data.discount,
        total=data.total,
        supplier_id=db_supplier.id
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    # 3. Guardar las líneas de la factura
    for item in data.items:
        db_item = models.InvoiceLine(
            **item.model_dump(), # Convierte el schema de Pydantic a diccionario
            invoice_id=new_invoice.id
        )
        db.add(db_item)
    
    db.commit()
    return {"message": "Factura y proveedor guardados correctamente", "id": new_invoice.id}