import fitz 
import httpx
import json
import re
import os
from schemas import InvoiceResponse

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_HOST}/api/generate"

async def process_pdf_to_json(file_content: bytes) -> InvoiceResponse:
    # 1. Extraer texto
    doc = fitz.open(stream=file_content, filetype="pdf")
    text = chr(12).join([page.get_text() for page in doc]) # chr(12) es salto de página

    # 2. Prompt ultra-específico basado en tus Schemas
    prompt = f"""
    Eres un extractor de datos contables de alta precisión. Analiza el texto de la factura y sigue estos pasos:
    
    1. Identifica al emisor y su CIF (busca patrones como B12345678). Ignora emails o webs.
    2. Lista los artículos. Si el precio es 0, busca si es un regalo o descuento.
    3. Verifica los totales: (Base Imponible + IVA - Descuento) debe ser igual al Total.
    
    REGLAS DE FORMATO:
    - `date`: Siempre DD/MM/YYYY.
    - `supplier_cif`: SOLO el código alfanumérico limpio sin simbolos.
    - `items`: La `tax` por item debe ser el porcentaje o el importe del impuesto de esa línea.
    - Solo devuelve el JSON, sin texto extra.

    FORMATO REQUERIDO:
    {{
        "supplier_name": "Nombre",
        "supplier_cif": "CIF",
        "ia_notes": "Cualquier anomalía o patrón detectado en esta factura",
        "date": "DD/MM/YYYY",
        "invoice_num": "000",
        "taxable_base": 0.0,
        "vat": 0.0,
        "discount": 0.0,
        "total": 0.0,
        "items": [
            {{
                "position": 1,
                "description": "Producto",
                "quantity": 1,
                "price": 0.0,
                "tax": 0.0,
                "discount": 0.0,
                "total_item": 0.0
            }}
        ]
    }}
    
    TEXTO:
    {text}
    """

    # 3. Llamada a Ollama
    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }, timeout=120.0)
        
        raw_json = response.json().get("response", "{}")

        # --- LIMPIEZA DE SEGURIDAD ---
        # 1. Eliminar posibles bloques de markdown si la IA los pone
        raw_json = re.sub(r'```json\s*|```', '', raw_json).strip()
        
        try:
            data_dict = json.loads(raw_json)

            # 2. VALIDACIÓN LÓGICA: Si la IA sumó mal, recalculamos nosotros
            # Calculamos la base imponible real sumando los items
            items = data_dict.get("items", [])
            real_base = sum(item.get("total_item", 0) for item in items)
            
            # Si la diferencia entre lo que dijo la IA y la realidad es mucha, corregimos
            if abs(data_dict.get("taxable_base", 0) - real_base) > 1:
                data_dict["taxable_base"] = round(real_base, 2)
            
            # Aseguramos que el Total sea coherente
            data_dict["total"] = round(data_dict["taxable_base"] + data_dict.get("vat", 0) - data_dict.get("discount", 0), 2)

            # 3. Limpieza de CIF (quitar emails si la IA falló)
            cif = data_dict.get("supplier_cif", "")
            if "@" in cif:
                # Intentamos extraer solo lo que parezca un CIF (Letra + 8 números)
                match = re.search(r'[ABCDEFGHJKLMNPQSVW]\d{8}', cif.upper())
                data_dict["supplier_cif"] = match.group(0) if match else cif

            # Validamos con Pydantic y devolvemos
            return InvoiceResponse(**data_dict)

        except Exception as e:
            print(f"ERROR EN PROCESAMIENTO: {e}")
            print(f"JSON RECIBIDO: {raw_json}")
            raise Exception(f"Error al validar datos de IA: {str(e)}")