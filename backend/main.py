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
from sqlalchemy import func, extract, cast, Date, text
from datetime import datetime

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
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Añade ambas variantes
    allow_credentials=True,
    allow_methods=["*"], # Usa "*" para permitir todos los verbos incluyendo DELETE y OPTIONS
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
        
        # 1. Extracción de texto
        doc = fitz.open(stream=content, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        # 2. Búsqueda de Memoria (CIF o Nombre)
        historical_context = ""
        cif_pattern = r'([ABCDEFGHJKLMNPQSVW][\s\.\-]?\d{8})|(\d{8}[\s\.\-]?[TRWAGMYFPDXBNJZSQVHLCKE])'
        cif_match = re.search(cif_pattern, full_text.upper())

        db_supplier = None
        if cif_match:
            clean_cif = re.sub(r'[^A-Z0-9]', '', cif_match.group(0))
            db_supplier = db.query(models.Supplier).filter(models.Supplier.cif == clean_cif).first()
        
        if not db_supplier:
            all_suppliers = db.query(models.Supplier).all()
            for s in all_suppliers:
                if s.name.upper() in full_text.upper():
                    db_supplier = s
                    break

        if db_supplier:
            # Inyectamos el CIF y las notas de memoria
            historical_context = f"Proveedor: {db_supplier.name}. CIF: {db_supplier.cif}. Notas: {db_supplier.ia_notes}"
            logger.info(f"Memoria inyectada para: {db_supplier.name}")

        # 3. Procesar con IA
        extracted_data = await process_pdf_to_json(full_text, context=historical_context)
        extracted_data.temp_file = temp_filename

        # --- NUEVA LÓGICA DE POST-PROCESAMIENTO MATEMÁTICO ---
        # Si hay un descuento mencionado en la memoria, forzamos el cálculo aquí
        if db_supplier and db_supplier.ia_notes:
            # Buscamos un patrón de porcentaje (ej: "10%") en las notas del proveedor
            pct_match = re.search(r'(\d+(?:\.\d+)?)\s*%', db_supplier.ia_notes)
            if pct_match:
                discount_pct = float(pct_match.group(1))
                
                # Recalculamos basándonos en los items extraídos
                subtotal_items = sum(item.quantity * item.price for item in extracted_data.items)
                
                # Aplicamos el descuento de memoria
                new_discount = round(subtotal_items * (discount_pct / 100), 2)
                extracted_data.discount = new_discount
                
                # Recalculamos Base e Imponible y Total
                extracted_data.taxable_base = round(subtotal_items - new_discount, 2)
                # El total es Base + IVA (asumiendo que el IVA extraído es correcto)
                extracted_data.total = round(extracted_data.taxable_base + extracted_data.vat, 2)
                
                extracted_data.ia_notes += f" [Cálculo: Dto {discount_pct}% aplicado por sistema]"

        # 4. Verificación final del proveedor
        final_supplier = db.query(models.Supplier).filter(
            models.Supplier.cif == extracted_data.supplier_cif
        ).first()
        
        return {
            "extracted": extracted_data,
            "temp_file": temp_filename, 
            "db_supplier": final_supplier,
            "is_new_supplier": final_supplier is None
        }

    except Exception as e:
        if os.path.exists(file_path): os.remove(file_path)
        logger.error(f"Error en backend: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-invoice/")
async def save_invoice(data: schemas.InvoiceResponse, db: Session = Depends(get_db)):
    try:
        # 1. Gestión del Proveedor
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

        # 2. Organización de carpetas
        clean_name = re.sub(r'[^a-zA-Z0-9]', '', data.supplier_name)
        folder_name = f"{clean_name}_{data.supplier_cif}"
        supplier_dir = os.path.join(UPLOAD_DIR, folder_name)
        if not os.path.exists(supplier_dir): 
            os.makedirs(supplier_dir)

        # 3. Lógica del PDF (Solo si es nuevo y viene de temp)
        # Intentamos obtener el ID si existe en el schema
        invoice_id = getattr(data, 'id', None)
        relative_pdf_path = getattr(data, 'pdf_path', None)

        if data.temp_file:
            clean_inv_num = data.invoice_num.replace("/", "-").replace(" ", "_")
            final_filename = f"Factura_{clean_inv_num}.pdf"
            absolute_pdf_path = os.path.join(supplier_dir, final_filename)
            relative_pdf_path = f"storage/{folder_name}/{final_filename}"

            temp_path = os.path.join(UPLOAD_DIR, data.temp_file) 
            if os.path.exists(temp_path):
                shutil.move(temp_path, absolute_pdf_path)

        # 4. Crear o Actualizar la Factura
        if invoice_id:
            # MODO EDICIÓN
            new_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
            if not new_invoice:
                raise HTTPException(status_code=404, detail="Factura no encontrada")
            
            new_invoice.invoice_num = data.invoice_num
            new_invoice.date_str = data.date
            new_invoice.taxable_base = data.taxable_base
            new_invoice.vat = data.vat
            new_invoice.discount = data.discount
            new_invoice.total = data.total
            # No sobreescribimos el path si no hay uno nuevo
            if relative_pdf_path:
                new_invoice.pdf_path = relative_pdf_path
        else:
            # MODO NUEVA FACTURA
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

        # 5. Guardar Líneas (Borramos las anteriores y creamos nuevas para evitar duplicados en edición)
        if invoice_id:
            db.query(models.InvoiceLine).filter(models.InvoiceLine.invoice_id == new_invoice.id).delete()

        for item in data.items:
            item_data = item.model_dump() if hasattr(item, 'model_dump') else item
            db_item = models.InvoiceLine(
                position=item_data.get('position'),
                description=item_data.get('description'),
                quantity=item_data.get('quantity'),
                price=item_data.get('price'),
                tax=float(item_data.get('tax', 0.0)), 
                discount=item_data.get('discount', 0.0),
                total_item=item_data.get('total_item'),
                invoice_id=new_invoice.id
            )
            db.add(db_item)
        
        db.commit()
        return {"message": "Operación exitosa", "pdf_url": new_invoice.pdf_path, "id": new_invoice.id}

    except Exception as e:
        db.rollback()
        logger.error(f"Error en save_invoice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/invoices/")
async def list_invoices(db: Session = Depends(get_db)):
    # Añadimos joinedload para los items/líneas de la factura
    return db.query(models.Invoice).options(
        joinedload(models.Invoice.supplier),
        joinedload(models.Invoice.items) # <--- Asegúrate que el nombre coincida con tu models.py
    ).all()

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

@app.put("/suppliers/{supplier_id}")
async def update_supplier(supplier_id: int, data: schemas.SupplierUpdate, db: Session = Depends(get_db)):
    db_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Actualizar campos dinámicamente
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_supplier, key, value)
    
    try:
        db.commit()
        db.refresh(db_supplier)
        return db_supplier
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar: {str(e)}")

@app.delete("/suppliers/{supplier_id}")
async def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Verificamos si tiene facturas asociadas para evitar errores de clave foránea
    invoice_count = db.query(models.Invoice).filter(models.Invoice.supplier_id == supplier_id).count()
    if invoice_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"No se puede borrar: Este proveedor tiene {invoice_count} facturas asociadas. Borra las facturas primero."
        )

    db.delete(db_supplier)
    db.commit()
    return {"message": "Proveedor eliminado correctamente"}


@app.get("/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    try:
        # 1. KPIs Básicos
        total_invoices = db.query(models.Invoice).count()
        total_spent_val = db.query(func.sum(models.Invoice.total)).scalar() or 0.0
        total_suppliers = db.query(models.Supplier).count()
        
        # Conteo físico de PDFs pendientes (los que están en la carpeta pero no en la DB)
        try:
            pending_files = [f for f in os.listdir(UPLOAD_DIR) 
                             if os.path.isfile(os.path.join(UPLOAD_DIR, f)) 
                             and f.lower().endswith('.pdf')]
            real_pending_count = len(pending_files)
        except Exception as e:
            real_pending_count = 0

        # --- LÓGICA DE INSIGHTS REALES ---
        insights_list = []
        
        # A. Detectar proveedor top
        top_supplier = db.query(
            models.Supplier.name, 
            func.sum(models.Invoice.total).label('total')
        ).join(models.Invoice).group_by(models.Supplier.name).order_by(text('total DESC')).first()

        if top_supplier:
            insights_list.append(f"El proveedor con mayor volumen de gasto es {top_supplier.name}.")
        
        # B. Detectar volumen de facturas
        insights_list.append(f"Se han registrado {total_invoices} facturas en el sistema.")

        # C. Detectar archivos sin procesar
        if real_pending_count > 0:
            insights_list.append(f"Hay {real_pending_count} facturas pendientes de ser procesadas en la carpeta de entrada.")
        else:
            insights_list.append("No hay archivos pendientes en la cola de procesamiento.")

        # 2. Datos para la Gráfica (Tu lógica actual)
        monthly_data = db.query(
            extract('month', cast(models.Invoice.date_str, Date)).label('month'),
            func.sum(models.Invoice.total).label('total')
        ).group_by('month').order_by('month').limit(6).all()

        months_names = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        chart_labels = [months_names[int(row.month) - 1] for row in monthly_data if row.month]
        chart_values = [float(row.total) for row in monthly_data if row.month]

        return {
            "kpis": {
                "total_spent": f"{total_spent_val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."),
                "processed_count": total_invoices,
                "suppliers_count": total_suppliers,
                "pending_count": real_pending_count  # <-- Ahora enviamos el real
            },
            "chart": {
                "labels": chart_labels if chart_labels else ["Sin datos"],
                "values": chart_values if chart_values else [0]
            },
            "insights": insights_list # Enviamos la lista de verdades
        }
    except Exception as e:
        logger.error(f"Error en dashboard stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    
# --- NUEVOS ENDPOINTS DE MANTENIMIENTO ---

@app.get("/api/db/export")
async def export_database(db: Session = Depends(get_db)):
    try:
        # Consultar toda la base de datos con sus relaciones
        suppliers = db.query(models.Supplier).options(
            joinedload(models.Supplier.invoices).joinedload(models.Invoice.items)
        ).all()

        export_data = {
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "suppliers": []
        }

        for s in suppliers:
            s_data = {
                "name": s.name,
                "cif": s.cif,
                "address": s.address,
                "ia_notes": s.ia_notes,
                "invoices": []
            }
            for inv in s.invoices:
                inv_data = {
                    "invoice_num": inv.invoice_num,
                    "date": inv.date_str,
                    "taxable_base": inv.taxable_base,
                    "vat": inv.vat,
                    "discount": inv.discount,
                    "total": inv.total,
                    "pdf_path": inv.pdf_path,
                    "items": [
                        {
                            "position": item.position,
                            "description": item.description,
                            "quantity": item.quantity,
                            "price": item.price,
                            "tax": item.tax,
                            "discount": item.discount,
                            "total_item": item.total_item
                        } for item in inv.items
                    ]
                }
                s_data["invoices"].append(inv_data)
            export_data["suppliers"].append(s_data)

        return export_data
    except Exception as e:
        logger.error(f"Error exportando DB: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al generar el backup")

@app.post("/api/db/import")
async def import_database(data: dict, db: Session = Depends(get_db)):
    try:
        # 1. Limpiar base de datos actual (Opcional, según prefieras)
        db.query(models.InvoiceLine).delete()
        db.query(models.Invoice).delete()
        db.query(models.Supplier).delete()
        
        # 2. Re-poblar desde el JSON
        for s_data in data.get("suppliers", []):
            db_supplier = models.Supplier(
                name=s_data["name"],
                cif=s_data["cif"],
                address=s_data["address"],
                ia_notes=s_data.get("ia_notes")
            )
            db.add(db_supplier)
            db.flush() # Para obtener el ID del proveedor

            for inv_data in s_data.get("invoices", []):
                db_invoice = models.Invoice(
                    invoice_num=inv_data["invoice_num"],
                    date_str=inv_data["date"],
                    taxable_base=inv_data["taxable_base"],
                    vat=inv_data["vat"],
                    discount=inv_data["discount"],
                    total=inv_data["total"],
                    pdf_path=inv_data.get("pdf_path"),
                    supplier_id=db_supplier.id
                )
                db.add(db_invoice)
                db.flush()

                for item_data in inv_data.get("items", []):
                    db_item = models.InvoiceLine(
                        **item_data,
                        invoice_id=db_invoice.id
                    )
                    db.add(db_item)
        
        db.commit()
        return {"success": True, "message": "Datos importados correctamente"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error importando DB: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al restaurar el backup")

@app.post("/api/maintenance/reindex")
async def reindex_files(db: Session = Depends(get_db)):
    # Simulación de re-indexación: contar archivos en storage
    try:
        files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
        # Aquí podrías añadir lógica para verificar si cada archivo está en la DB
        return {"success": True, "count": len(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/db/clear")
async def clear_database(db: Session = Depends(get_db)):
    try:
        db.query(models.InvoiceLine).delete()
        db.query(models.Invoice).delete()
        db.query(models.Supplier).delete()
        db.commit()
        return {"success": True, "message": "Todos los registros han sido eliminados"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))