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

    # 2. Prompt ultra-específico refinado para detección de columnas
    prompt = f"""
    Eres un extractor de datos contables de alta precisión y auditor de facturas. Tu objetivo es mapear el texto a un JSON estructurado y detectar discrepancias.

    REGLAS DE ORO PARA COLUMNAS:
    1. El primer número de la fila suele ser la CANTIDAD (quantity).
    2. El texto central es la DESCRIPCIÓN (description).
    3. El número a la derecha de la descripción es el PRECIO UNITARIO (price).
    4. El último número de la fila es el TOTAL DE LÍNEA (total_item).

    LÓGICA DE AUDITORÍA CRÍTICA:
    - Compara: (taxable_base + vat - discount) vs total.
    - Si hay discrepancias o falta información clave (como el CIF), REDACTA un aviso breve y directo en `ia_notes`.
    - NO uses frases como "Se debe indicar" o "He encontrado". 
    - USA mensajes directos: "Falta el CIF del proveedor", "El total no coincide con la suma de los conceptos".

    PASOS DE PROCESAMIENTO:
    - Identifica al emisor y su CIF. Si no hay CIF, indícalo en `ia_notes`.
    - Extrae la fecha en formato DD/MM/YYYY.
    - Para cada item: Verifica que (quantity * price) ≈ total_item.

    REGLAS DE FORMATO:
    - `supplier_cif`: Sin espacios ni guiones.
    - `tax`: Porcentaje de IVA (ej. 21.0).
    - Solo devuelve el JSON puro, sin bloques de código ni texto adicional.

    FORMATO REQUERIDO:
    {{
        "supplier_name": "Nombre",
        "supplier_cif": "CIF",
        "ia_notes": "Aquí escribe cualquier error de cálculo, falta de CIF o anomalía detectada",
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
                "quantity": 0.0,
                "price": 0.0,
                "tax": 0.0,
                "discount": 0.0,
                "total_item": 0.0
            }}lla 
        ]
    }}

    TEXTO DE LA FACTURA:
    \"\"\"
    {text}
    \"\"\"
    """

    # 3. Llamada a Ollama
    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json={
            "model": "deepseek-r1:1.5b",
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,    # Determinismo total para facturas
                "num_ctx": 4000,     # Contexto suficiente para un PDF
                "top_p": 0.9
            }
            
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