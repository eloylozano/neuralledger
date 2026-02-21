from pydantic import BaseModel
from typing import List

class InvoiceItem(BaseModel):
    position: int
    descripcion: str
    quantity: int 
    price: float
    tax: float
    discount: float
    total_item: float

class InvoiceResponse(BaseModel):
    supplier_name: str
    supplier_cif: str
    date: str
    invoice_num: str
    taxable_base: float
    vat: float
    discount: float
    total: float
    items: List[InvoiceItem]