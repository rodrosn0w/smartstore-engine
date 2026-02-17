from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.post("/registrar")
def registrar_venta(pedido: schemas.VentaCreate, db: Session = Depends(get_db)):
    # 1. Buscar producto (el "escaneo")
    producto = db.query(models.Producto).filter(models.Producto.id == pedido.producto_id).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # 2. Validar stock
    if producto.stock < pedido.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")
    
    # 3. Calcular Total y Vuelto
    total = producto.precio * pedido.cantidad
    vuelto = pedido.pago_con - float(total)
    
    if vuelto < 0:
        raise HTTPException(status_code=400, detail=f"Faltan {abs(vuelto)} para completar el pago")
    
    # 4. Registrar la venta en DB
    nueva_venta = models.Venta(total=total, metodo_pago="efectivo")
    db.add(nueva_venta)
    db.flush() 
    
    # 5. Descontar stock
    producto.stock -= pedido.cantidad
    db.commit()
    
    return {
        "mensaje": "Venta exitosa",
        "producto": producto.nombre,
        "total_a_pagar": total,
        "pago_con": pedido.pago_con,
        "vuelto": vuelto,
        "stock_restante": producto.stock
    }