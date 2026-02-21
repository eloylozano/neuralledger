from pydantic import BaseModel
from typing import List, Optional

class InvoiceItem(BaseModel):
    position: int
    description: str
    quantity: int 
    price: float
    ia_notes: Optional[float] = 0.0
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
    ia_notes: Optional[str] = ""
    items: List[InvoiceItem]
    