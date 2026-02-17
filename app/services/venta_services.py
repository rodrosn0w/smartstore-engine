# app/services/ventas_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas

class VentasService:
    @staticmethod
    def procesar_registro_venta(db: Session, pedido: schemas.VentaCreate):
        # 1. Buscar producto (Escaneo)
        producto = db.query(models.Producto).filter(models.Producto.id == pedido.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # 2. Validar stock
        if producto.stock < pedido.cantidad:
            raise HTTPException(status_code=400, detail="Stock insuficiente")

        # 3. Lógica de dinero
        total = producto.precio * pedido.cantidad
        vuelto = pedido.pago_con - float(total)
        
        if vuelto < 0:
            raise HTTPException(status_code=400, detail=f"Faltan {abs(vuelto)} para completar el pago")

        # 4. Impactar Base de Datos
        nueva_venta = models.Venta(total=total)
        db.add(nueva_venta)
        producto.stock -= pedido.cantidad
        
        db.commit()
        db.refresh(nueva_venta)

        return {
            "producto": producto.nombre,
            "total": total,
            "vuelto": vuelto,
            "stock_restante": producto.stock
        }