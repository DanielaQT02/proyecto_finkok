from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, TIMESTAMP, Text, Numeric, Boolean
from sqlalchemy.orm import relationship  
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    role = Column(String)
    active = Column(Boolean, default=True)

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String)
    taxpayer_id = Column(String)
    # Aquí ya no marcará error porque ya importamos relationship
    invoices = relationship("Invoice", back_populates="owner")

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    buffer_id = Column(BigInteger, index=True) 
    response_code = Column(String)
    message = Column(Text)
    taxpayer_id = Column(String, index=True) 
    rtaxpayer_id = Column(String)            
    total = Column(Numeric(12, 2))
    xml_timbrado = Column(String)            
    uuid = Column(String, unique=True, index=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    
    # También necesitamos la relación inversa aquí
    business_id = Column(Integer, ForeignKey("businesses.id"))
    owner = relationship("Business", back_populates="invoices")

class StampingBatch(Base):
    __tablename__ = "stamping_batches"
    id = Column(Integer, primary_key=True, index=True)
    zip_name = Column(String)
    total_xml = Column(Integer)
    status = Column(String)