from sqlalchemy.orm import Session, selectinload
from .models import Invoice, Business, User, ErrorStamping, StampingBatch, StampingStatistic

class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_invoice_by_uuid(self, uuid: str):
        return self.db.query(Invoice).options(selectinload(Invoice.owner)).filter(Invoice.uuid == uuid).first()

    def get_all_invoices(self):
        return self.db.query(Invoice).options(selectinload(Invoice.owner)).all()

    def create_invoice(self, invoice_data: dict):
        db_invoice = Invoice(**invoice_data)
        self.db.add(db_invoice)
        self.db.commit()
        self.db.refresh(db_invoice)
        return db_invoice

    def update_invoice(self, uuid: str, invoice_data: dict):
        db_invoice = self.db.query(Invoice).filter(Invoice.uuid == uuid).first()
        if db_invoice:
            for key, value in invoice_data.items():
                if key == 'uuid': continue # Protegemos el UUID para evitar error 500
                setattr(db_invoice, key, value)
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

    def create_business(self, biz_data: dict):
        db_biz = Business(**biz_data)
        self.db.add(db_biz)
        self.db.commit()
        self.db.refresh(db_biz)
        return db_biz

    def get_all_businesses(self):
        return self.db.query(Business).all()

    def get_business_by_id(self, biz_id: int):
        return self.db.query(Business).filter(Business.id == biz_id).first()

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

class ErrorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_errors_by_invoice(self, uuid: str):
        return self.db.query(ErrorStamping).filter(ErrorStamping.invoice_uuid == uuid).all()

    def create_error(self, error_data: dict):
        db_error = ErrorStamping(**error_data)
        self.db.add(db_error)
        self.db.commit()
        self.db.refresh(db_error)
        return db_error