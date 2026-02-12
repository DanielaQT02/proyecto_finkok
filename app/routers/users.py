from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repository import UserRepository
from app import schemas

router = APIRouter(prefix="/users", tags=["Users"])

# --- CREAR ---
@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en el sistema."""
    repo = UserRepository(db)
    # Validar que el email no exista previamente
    existing_user = repo.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado en el sistema"
        )
    return repo.create_user(user.model_dump())

# --- LEER (TODOS) ---
@router.get("/", response_model=list[schemas.User])
def list_users(db: Session = Depends(get_db)):
    """Lista todos los usuarios registrados en el sistema."""
    repo = UserRepository(db)
    return repo.get_all_users()

# --- LEER (UNO) ---
@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene los detalles de un usuario específico por su ID."""
    repo = UserRepository(db)
    db_user = repo.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# --- ACTUALIZAR ---
@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """Actualiza la información de un usuario (email, rol, estado activo)."""
    repo = UserRepository(db)
    
    # Validar que el usuario exista
    db_user = repo.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Si se está actualizando el email, validar que no exista otro usuario con ese email
    if user.email and user.email != db_user.email:
        existing_user = repo.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="El email ya está registrado por otro usuario"
            )
    
    updated_user = repo.update_user(user_id, user.model_dump(exclude_unset=True))
    return updated_user

# --- ELIMINAR ---
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario del sistema."""
    repo = UserRepository(db)
    if not repo.delete_user(user_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None
