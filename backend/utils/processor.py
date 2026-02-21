import fitz 
import httpx
import json
from schemas import InvoiceResponse

OLLAMA_URL = "http://localhost:11434/api/generate"

async def process_pdf_to_json(file_content: bytes) -> InvoiceResponse:
    # 1. Extraer texto
    doc = fitz.open(stream=file_content, filetype="pdf")
    text = chr(12).join([page.get_text() for page in doc]) # chr(12) es salto de página

    # 2. Prompt ultra-específico basado en tus Schemas
    prompt = f"""
    Eres un extractor de datos contables de alta precisión. Tu objetivo es convertir el texto de una factura en un JSON válido.
    
    ### REGLAS DE ORO:
    1. **Respuesta Limpia**: Devuelve ÚNICAMENTE el objeto JSON. No incluyas explicaciones, ni etiquetas de código Markdown.
    2. **Tipos de Datos**: Los campos numéricos (taxable_base, vat, total, price, etc.) deben ser números (float), nunca strings con símbolos de moneda.
    3. **Limpieza de CIF**: El 'supplier_cif' debe contener solo el identificador fiscal (ej. B12345678). Elimina emails o direcciones que aparezcan cerca.
    4. **Coherencia Matemática**: 
       - total = taxable_base + vat - discount.
       - total_item = quantity * price - discount (por cada item).
       - Verifica estas sumas antes de generar el JSON. Si algo no cuadra, corrígelo basándote en el 'total' de la factura.
    5. **Fecha**: Formato estrictamente DD/MM/YYYY.

    ### FORMATO JSON REQUERIDO:
    {{
        "supplier_name": "Nombre exacto",
        "supplier_cif": "CIF_LIMPIO",
        "date": "DD/MM/YYYY",
        "invoice_num": "String del numero",
        "taxable_base": 0.0,
        "vat": 0.0,
        "discount": 0.0,
        "total": 0.0,
        "items": [
            {{
                "position": 1,
                "descripcion": "Texto",
                "quantity": 1,
                "price": 0.0,
                "tax": 0.0,
                "discount": 0.0,
                "total_item": 0.0
            }}
        ]
    }}

    TEXTO A PROCESAR:
    {text}
    """

    # 3. Llamada a Ollama
    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }, timeout=60.0)
        
        # 4. Convertimos la respuesta string en un objeto de Python
        data_dict = json.loads(response.json()["response"])
        
        # 5. Validamos con tu Schema de Pydantic
        return InvoiceResponse(**data_dict)