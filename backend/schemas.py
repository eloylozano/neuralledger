from pydantic import BaseModel
from typing import List, Optional

class InvoiceItem(BaseModel):
    position: int
    description: str
    quantity: float # Cambiado a float por si hay pesos (2.5kg)
    price: float
    tax: Optional[float] = 0.0 # Añadido: Lo necesitas en main.py
    ia_notes: Optional[str] = "" 
    discount: float
    total_item: float

class InvoiceResponse(BaseModel):
    id: Optional[int] = None
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
    temp_file: Optional[str] = None
    
class SupplierResponse(BaseModel):
    id: int
    name: str
    cif: str
    address: str
    ia_notes: Optional[str] = None
    invoice_count: int
    total_spent: float

    class Config:
        from_attributes = True
        
        
class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    cif: Optional[str] = None
    address: Optional[str] = None
    ia_notes: Optional[str] = None

    class Config:
        from_attributes = True