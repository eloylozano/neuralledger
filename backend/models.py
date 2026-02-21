from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    cif = Column(String, unique=True, index=True, nullable=False)
    # Aquí la IA podría guardar "notas" sobre cómo procesar este proveedor
    ia_notes = Column(String, nullable=True)
    
    invoices = relationship("Invoice", back_populates="supplier")

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_num = Column(String, index=True)
    date_str = Column(String) # Guardamos la fecha que leyó la IA
    created_at = Column(DateTime, server_default=func.now())
    
    taxable_base = Column(Float)
    vat = Column(Float)
    discount = Column(Float)
    total = Column(Float)
    pdf_path = Column(String) # Ruta al archivo en /backend/storage/

    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    supplier = relationship("Supplier", back_populates="invoices")
    
    # Relación para los items detallados
    items = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceLine(Base):
    __tablename__ = "invoice_lines"
    id = Column(Integer, primary_key=True, index=True)
    position = Column(Integer)
    description = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    tax = Column(Float)
    discount = Column(Float)
    total_item = Column(Float)
    
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    invoice = relationship("Invoice", back_populates="items")