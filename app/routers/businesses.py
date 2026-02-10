from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository import BusinessRepository
from .. import schemas

router = APIRouter(prefix="/businesses", tags=["Businesses"])

@router.post("/", response_model=schemas.Business, status_code=status.HTTP_201_CREATED)
def create_business(business: schemas.BusinessBase, db: Session = Depends(get_db)):
    """Crea una nueva empresa en el sistema."""
    repo = BusinessRepository(db)
    return repo.create_business(business.model_dump())

@router.get("/", response_model=list[schemas.Business])
def list_businesses(db: Session = Depends(get_db)):
    """Lista todas las empresas registradas."""
    repo = BusinessRepository(db)
    return repo.get_all_businesses()
@router.get("/{business_id}/invoices", response_model=list[schemas.Invoice])
def read_business_invoices(business_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todas las facturas que pertenecen a una empresa específica.
    """
    repo_biz = BusinessRepository(db)
    # Primero verificamos si la empresa existe
    if not repo_biz.get_business_by_id(business_id):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    return repo_biz.get_invoices_by_business(business_id)