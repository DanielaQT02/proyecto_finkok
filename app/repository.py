from sqlalchemy.orm import Session
from . import models
from .models import Invoice, StampingBatch, User
from .models import Business

class StampingRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_batches(self):
        return self.db.query(StampingBatch).all()
    
    def get_batch_by_id(self, batch_id: int):
        return self.db.query(StampingBatch).filter(StampingBatch.id == batch_id).first()

    def create_user(self, email: str, role: str):
        db_user = User(email=email, role=role)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    # Buscar factura por UUID específico
    def get_invoice_by_uuid(self, uuid: str):
        return self.db.query(Invoice).filter(Invoice.uuid == uuid).first()

    # Listar todas las facturas
    def get_all_invoices(self):
        return self.db.query(Invoice).all()

    # Crear nueva factura
    def create_invoice(self, invoice_data: dict):
        db_invoice = Invoice(**invoice_data)
        self.db.add(db_invoice)
        self.db.commit()
        self.db.refresh(db_invoice)
        return db_invoice

    def delete_invoice(self, uuid: str):
        db_invoice = self.db.query(Invoice).filter(Invoice.uuid == uuid).first()
        if db_invoice:
            self.db.delete(db_invoice)
            self.db.commit()
            return True
        return False


class BusinessRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_invoices_by_business(self, biz_id: int):
        # Usamos selectinload para cargar las facturas sin entrar en bucle
        return self.db.query(Invoice).filter(Invoice.business_id == biz_id).all()

    def __init__(self, db: Session):
        self.db = db

    def create_business(self, biz_data: dict):
        db_biz = Business(**biz_data)
        self.db.add(db_biz)
        self.db.commit()
        self.db.refresh(db_biz)
        return db_biz

    def get_all_businesses(self):
        return self.db.query(Business).all()

    def get_invoices_by_business(self, biz_id: int):
        return self.db.query(Invoice).filter(Invoice.business_id == biz_id).all() 
    
    def update_business(self, biz_id: int, biz_data: dict):
        db_biz = self.db.query(Business).filter(Business.id == biz_id).first()
        if db_biz:
            for key, value in biz_data.items():
                setattr(db_biz, key, value)
            self.db.commit()
            self.db.refresh(db_biz)
        return db_biz

    def delete_business(self, biz_id: int):
        db_biz = self.db.query(Business).filter(Business.id == biz_id).first()
        if db_biz:
            self.db.delete(db_biz)
            self.db.commit()
            return True
        return False