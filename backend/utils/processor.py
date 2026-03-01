import httpx
import json
import re
import os
from schemas import InvoiceResponse

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_HOST}/api/generate"

async def process_pdf_to_json(full_text: str, context: str = "") -> InvoiceResponse:
    # 1. Prompt refinado
    prompt = f"""
    Eres un auditor contable. Extrae los datos de esta factura a JSON.
    
    MEMORIA IMPORTANTE PARA ESTE PROVEEDOR:
    \"\"\"
    {context if context else "No hay instrucciones previas."}
    \"\"\"

    REGLAS:
    - CIF: Solo letras y números.
    - IA_NOTES: Si usaste la MEMORIA, indícalo aquí. Si faltan datos, anótalo.
    - Formato: Solo JSON puro.

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
                "num_ctx": 4096,
                "num_predict": 800  # Limita la longitud para ganar velocidad
            }
        }, timeout=120.0)
        
        raw_json = response.json().get("response", "{}")
        raw_json = re.sub(r'```json\s*|```', '', raw_json).strip()
        
        try:
            data_dict = json.loads(raw_json)

            # Validación de sumas
            items = data_dict.get("items", [])
            real_base = sum(item.get("total_item", 0) for item in items)
            
            if abs(data_dict.get("taxable_base", 0) - real_base) > 1:
                data_dict["taxable_base"] = round(real_base, 2)
            
            data_dict["total"] = round(data_dict["taxable_base"] + data_dict.get("vat", 0) - data_dict.get("discount", 0), 2)

            # Normalización final de CIF
            cif = data_dict.get("supplier_cif", "")
            data_dict["supplier_cif"] = re.sub(r'[^A-Z0-9]', '', cif.upper())

            return InvoiceResponse(**data_dict)

        except Exception as e:
            print(f"JSON RECIBIDO: {raw_json}")
            raise Exception(f"Error en validación IA: {str(e)}")