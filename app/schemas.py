from pydantic import BaseModel
from typing import List, Optional

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int
    categoria: Optional[str] = None

class VentaCreate(BaseModel):
    producto_id: int
    cantidad: int