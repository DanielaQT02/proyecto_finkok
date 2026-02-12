from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- ESQUEMAS DE USUARIO Y AUTH ---
class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    active: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- ESQUEMAS DE EMPRESA (BUSINESS) ---
class BusinessBase(BaseModel):
    taxpayer_id: str
    business_name: str

class Business(BusinessBase):
    id: int
    class Config:
        from_attributes = True

# --- ESQUEMAS DE FACTURA (INVOICE) ---
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
    business_id: int

class InvoiceUpdate(BaseModel):
    total: Optional[Decimal] = None
    response_code: Optional[str] = None
    message: Optional[str] = None
    xml_timbrado: Optional[str] = None

class Invoice(InvoiceBase):
    id: int
    created_at: datetime
    business_id: int
    owner: Optional[Business] = None 
    class Config:
        from_attributes = True

# --- ESQUEMAS DE ERRORES ---
class ErrorStamping(BaseModel):
    id: int
    invoice_uuid: str
    error_code: str
    error_message: str
    error_stage: str
    created_at: datetime
    class Config:
        from_attributes = True