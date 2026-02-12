from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repository import ErrorRepository
from app import schemas

router = APIRouter(prefix="/errors", tags=["Errors"])

@router.get("/{uuid}", response_model=list[schemas.ErrorStamping])
def get_invoice_errors(uuid: str, db: Session = Depends(get_db)):
    repo = ErrorRepository(db)
    return repo.get_errors_by_invoice(uuid)