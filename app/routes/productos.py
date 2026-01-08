from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

# Aquí definimos el router
router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/")
def listar_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()

@router.get("/reporte-critico")
def analizar_stock(db: Session = Depends(get_db)):
    bajos = db.query(models.Producto).filter(models.Producto.stock < 10).all()
    return {
        "analisis": "Inventario Crítico Detectado",
        "items": bajos
    }