import httpx
import json
import re
import os
from schemas import InvoiceResponse

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_HOST}/api/generate"

async def process_pdf_to_json(full_text: str, context: str = "") -> InvoiceResponse:
    prompt = f"""
    Eres un auditor contable experto. Tu objetivo es extraer datos exactos de facturas.
    
    [MEMORIA DEL SISTEMA - PRIORIDAD ALTA]
    {f"DATOS CONOCIDOS DEL PROVEEDOR: {context}" if context else "No hay datos previos."}

    [REGLAS CRÍTICAS]
    1. CIF: Si la MEMORIA indica un CIF, USA ESE. No inventes uno nuevo de emails o webs.
    2. IA_NOTES: Si usaste la MEMORIA para corregir datos, indícalo aquí.
    3. Si el texto del PDF es contradictorio con la MEMORIA, prioriza la MEMORIA.

    JSON REQUERIDO:
    {{
        "supplier_name": "Nombre",
        "supplier_cif": "CIF",
        "ia_notes": "...",
        "date": "DD/MM/YYYY",
        "invoice_num": "000",
        "taxable_base": 0.0,
        "vat": 0.0,
        "discount": 0.0,
        "total": 0.0,
        "items": [
            {{
                "position": 1,
                "description": "...",
                "quantity": 0.0,
                "price": 0.0,
                "tax": 0.0,
                "discount": 0.0,
                "total_item": 0.0
            }}
        ]
    }}

    TEXTO DE FACTURA:
    {full_text[:4000]}
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
                "num_ctx": 4096
            }
        }, timeout=120.0)
        
        raw_json = response.json().get("response", "{}")
        raw_json = re.sub(r'```json\s*|```', '', raw_json).strip()
        
        try:
            data_dict = json.loads(raw_json)

            # Validación de sumas básica
            items = data_dict.get("items", [])
            real_base = sum(item.get("total_item", 0) for item in items)
            if real_base > 0 and abs(data_dict.get("taxable_base", 0) - real_base) > 1:
                data_dict["taxable_base"] = round(real_base, 2)
            
            # Normalización de CIF
            cif = data_dict.get("supplier_cif", "")
            clean_cif = re.sub(r'[^A-Z0-9]', '', cif.upper())

            # REFUERZO: Si tenemos contexto y la IA falló el CIF, lo restauramos
            if context and (len(clean_cif) > 12 or len(clean_cif) < 5):
                match_in_context = re.search(r'[A-Z0-9]{8,10}', context)
                if match_in_context:
                    clean_cif = match_in_context.group(0)
                    data_dict["ia_notes"] = (data_dict.get("ia_notes", "") + " | CIF recuperado de memoria").strip()

            data_dict["supplier_cif"] = clean_cif
            
            # IMPORTANTE: El return que faltaba
            return InvoiceResponse(**data_dict)

        except Exception as e:
            print(f"JSON RECIBIDO: {raw_json}")
            raise Exception(f"Error en validación IA: {str(e)}")