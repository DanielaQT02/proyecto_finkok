from sqlalchemy import Column, Integer, String, Boolean, BigInteger, ForeignKey, TIMESTAMP, Text, Numeric
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    active = Column(Boolean, default=True)

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String)
    taxpayer_id = Column(String)
    
    invoices = relationship("Invoice", back_populates="owner")
    statistics = relationship("StampingStatistic", back_populates="owner")

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
    business_id = Column(Integer, ForeignKey("businesses.id"))
    owner = relationship("Business", back_populates="invoices")
    errors = relationship("ErrorStamping", back_populates="invoice")

class StampingBatch(Base):
    __tablename__ = "stamping_batches"
    id = Column(Integer, primary_key=True, index=True)
    zip_name = Column(String)
    total_xml = Column(Integer)
    status = Column(String)

class StampingStatistic(Base):
    __tablename__ = "stamping_statistics"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    month = Column(String) 
    stamped_success = Column(Integer, default=0)
    stamped_error = Column(Integer, default=0)
    
    owner = relationship("Business", back_populates="statistics")

class ErrorStamping(Base):
    __tablename__ = "errors_stamping"
    id = Column(Integer, primary_key=True, index=True)
    invoice_uuid = Column(String, ForeignKey("invoices.uuid"))
    error_code = Column(String)
    error_message = Column(Text)
    error_stage = Column(String) 
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    invoice = relationship("Invoice", back_populates="errors")