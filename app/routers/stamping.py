from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository import InvoiceRepository
from .. import schemas

router = APIRouter(prefix="/stamping", tags=["Stamping"])

# Obtener una factura específica por UUID
@router.get("/invoices/{uuid}", response_model=schemas.Invoice, status_code=status.HTTP_200_OK)
def read_invoice(uuid: str, db: Session = Depends(get_db)):
    repo = InvoiceRepository(db)
    db_invoice = repo.get_invoice_by_uuid(uuid)
    if db_invoice is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Factura con UUID {uuid} no encontrada"
        )
    return db_invoice

# Listar todas las facturas (200 OK)
@router.get("/invoices", response_model=list[schemas.Invoice], status_code=status.HTTP_200_OK)
def list_invoices(db: Session = Depends(get_db)):
    repo = InvoiceRepository(db)
    return repo.get_all_invoices()

# Crear factura (201 Created)
@router.post("/invoices/", response_model=schemas.Invoice, status_code=status.HTTP_201_CREATED)
def create_new_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    repo = InvoiceRepository(db)
    if repo.get_invoice_by_uuid(invoice.uuid):
        raise HTTPException(status_code=400, detail="El UUID ya está registrado")
    return repo.create_invoice(invoice.model_dump())