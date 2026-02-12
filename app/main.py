from fastapi import FastAPI
from app.database import engine, Base
# 1. Asegúrate de incluir 'auth' y que los nombres coincidan con tus archivos físicos
from app.routers import auth, stamping, businesses, errors

# Crea las tablas (incluyendo la de Users con hashed_password)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finkok Stamping Monitor API",
    description="API para el monitoreo y gestión de timbrado de CFDI para socios de negocio.",
    version="1.0.0"
)

# 2. Registro de Routers con el nombre correcto (.router)
app.include_router(auth.router)       
app.include_router(businesses.router)
app.include_router(stamping.router)
app.include_router(errors.router)      # Log de errores

@app.get("/")
def root():
    return {
        "status": "online",
        "project": "Finkok Residency Monitoring Platform",
        "location": "Morelia, Michoacán"
    }