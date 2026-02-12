from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Usamos importaciones absolutas para evitar errores de paquetes
from app.database import get_db
from app.repository import BusinessRepository
from app import schemas

router = APIRouter(prefix="/businesses", tags=["Businesses"])

# --- CREAR ---
@router.post("/", response_model=schemas.Business, status_code=status.HTTP_201_CREATED)
def create_business(business: schemas.BusinessBase, db: Session = Depends(get_db)):
    """Registra una nueva empresa o socio de negocio."""
    repo = BusinessRepository(db)
    return repo.create_business(business.model_dump())

# --- LEER (TODOS) ---
@router.get("/", response_model=list[schemas.Business])
def list_businesses(db: Session = Depends(get_db)):
    """Lista todas las empresas registradas."""
    repo = BusinessRepository(db)
    return repo.get_all_businesses()

# --- LEER (UNO) ---
@router.get("/{business_id}", response_model=schemas.Business)
def read_business(business_id: int, db: Session = Depends(get_db)):
    """Obtiene los detalles de una empresa específica por su ID."""
    repo = BusinessRepository(db)
    db_biz = repo.get_business_by_id(business_id)
    if not db_biz:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return db_biz

# --- ACTUALIZAR ---
@router.put("/{business_id}", response_model=schemas.Business)
def update_business(business_id: int, business: schemas.BusinessBase, db: Session = Depends(get_db)):
    """Actualiza la información de una empresa (RFC o Nombre)."""
    repo = BusinessRepository(db)
    updated_biz = repo.update_business(business_id, business.model_dump())
    if not updated_biz:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return updated_biz

# --- ELIMINAR ---
@router.delete("/{business_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business(business_id: int, db: Session = Depends(get_db)):
    """Elimina una empresa del sistema."""
    repo = BusinessRepository(db)
    if not repo.delete_business(business_id):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return None

# --- OBTENER FACTURAS DE LA EMPRESA ---
@router.get("/{business_id}/invoices", response_model=list[schemas.Invoice])
def read_business_invoices(business_id: int, db: Session = Depends(get_db)):
    """Lista todas las facturas que pertenecen a esta empresa."""
    repo_biz = BusinessRepository(db)
    if not repo_biz.get_business_by_id(business_id):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    return repo_biz.get_invoices_by_business(business_id)