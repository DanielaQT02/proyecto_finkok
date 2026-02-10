from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- ESQUEMAS PARA BUSINESS (EMPRESAS) ---

class BusinessBase(BaseModel):
    taxpayer_id: str
    business_name: str

class BusinessCreate(BusinessBase):
    pass

class Business(BusinessBase):
    id: int

    class Config:
        from_attributes = True


# --- ESQUEMAS PARA INVOICE (FACTURAS) ---

class InvoiceBase(BaseModel):
    taxpayer_id: str
    rtaxpayer_id: str
    total: Decimal
    uuid: str
    xml_timbrado: Optional[str] = None
    response_code: Optional[str] = None
    message: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    buffer_id: int
    business_id: int # ID de la empresa a la que pertenece

class Invoice(InvoiceBase):
    id: int
    created_at: datetime
    business_id: int
    # Incluimos la información de la empresa (Dueño)
    owner: Optional[Business] = None 

    class Config:
        from_attributes = True


# --- ESQUEMAS PARA STAMPING BATCHES (LOTES) ---

class StampingBatchBase(BaseModel):
    zip_name: str
    total_xml: int
    status: str

class StampingBatch(StampingBatchBase):
    id: int

    class Config:
        from_attributes = True