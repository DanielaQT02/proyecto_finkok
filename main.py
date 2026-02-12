from fastapi import FastAPI
from app.database import engine, Base
from fastapi.security import OAuth2PasswordBearer
from app.routers import auth, stamping, businesses, errors

# Crea todas las tablas, incluyendo la nueva tabla de 'users'
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finkok Stamping Monitor API",
    version="1.0.0",
    # Esto ayuda a Swagger a entender dónde está el login
)

# Registro de Routers
# El de auth debe ir preferentemente al inicio para que sea lo primero que veas en Swagger
app.include_router(auth.router)
app.include_router(businesses.router)
app.include_router(stamping.router)
app.include_router(errors.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "project": "Finkok Residency Monitoring Platform",
        "location": "Morelia, Michoacán"
    }