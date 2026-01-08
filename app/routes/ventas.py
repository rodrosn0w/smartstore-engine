from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.post("/registrar")
def registrar_venta(pedido: schemas.VentaCreate, db: Session = Depends(get_db)):
    # 1. Buscar producto
    producto = db.query(models.Producto).filter(models.Producto.id == pedido.producto_id).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # 2. Validar stock antes de vender
    if producto.stock < pedido.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente para esta operación")
    
    # 3. Registrar la venta
    total = producto.precio * pedido.cantidad
    nueva_venta = models.Venta(total=total)
    db.add(nueva_venta)
    db.flush() 
    
    # 4. Descontar stock y guardar
    producto.stock -= pedido.cantidad
    db.commit()
    
    return {"mensaje": "Venta exitosa", "total": total, "stock_restante": producto.stock}