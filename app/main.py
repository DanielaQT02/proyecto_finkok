from fastapi import FastAPI
from .database import engine, Base
from .routers import stamping, businesses

# Creamos las tablas en la DB (finkok.db)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Monitoreo Finkok")

# Registramos el router
app.include_router(stamping.router)
app.include_router(businesses.router)

@app.get("/")
def home():
    return {"message": "API de Gestión de Timbrado lista"}
