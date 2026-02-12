from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repository import InvoiceRepository
from app import schemas
from app.auth_utils import oauth2_scheme

router = APIRouter(prefix="/stamping", tags=["Stamping"])

# --- CREAR FACTURA (POST) ---
@router.post("/invoices/", response_model=schemas.Invoice, status_code=status.HTTP_201_CREATED)
def create_new_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    """
    Registra una nueva factura vinculada a una empresa.
    Valida que el UUID no exista previamente.
    """
    repo = InvoiceRepository(db)
    if repo.get_invoice_by_uuid(invoice.uuid):
        raise HTTPException(
            status_code=400, 
            detail="El UUID ya está registrado en el sistema"
        )
    return repo.create_invoice(invoice.model_dump())

# --- LISTAR TODAS (GET) ---
from app.auth_utils import oauth2_scheme # Importa el esquema

@router.get("/invoices", response_model=list[schemas.Invoice])
def list_invoices(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme) 
):
    repo = InvoiceRepository(db)
    return repo.get_all_invoices()

# --- OBTENER UNA POR UUID (GET) ---
@router.get("/invoices/{uuid}", response_model=schemas.Invoice, status_code=status.HTTP_200_OK)
def read_invoice(uuid: str, db: Session = Depends(get_db)):
    """
    Busca una factura específica usando su Folio Fiscal (UUID).
    """
    repo = InvoiceRepository(db)
    db_invoice = repo.get_invoice_by_uuid(uuid)
    if not db_invoice:
        raise HTTPException(
            status_code=404, 
            detail=f"Factura con UUID {uuid} no encontrada"
        )
    return db_invoice

# --- ACTUALIZAR FACTURA (PUT) ---
@router.put("/invoices/{uuid}", response_model=schemas.Invoice)
def update_invoice(uuid: str, invoice_update: schemas.InvoiceUpdate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de una factura existente (útil para corregir montos o mensajes de respuesta).
    """
    repo = InvoiceRepository(db)
    
    updated_invoice = repo.update_invoice(uuid, invoice_update.model_dump())
    if not updated_invoice:
        raise HTTPException(status_code=404, detail="Factura no encontrada para actualizar")
    return updated_invoice

# --- ELIMINAR FACTURA (DELETE) ---
@router.delete("/invoices/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(uuid: str, db: Session = Depends(get_db)):
    """
    Elimina permanentemente una factura del registro.
    """
    repo = InvoiceRepository(db)
    if not repo.delete_invoice(uuid):
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return None

