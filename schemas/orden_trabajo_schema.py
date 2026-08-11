from pydantic import BaseModel, field_validator
from typing import Optional

class OrdenTrabajoCrear(BaseModel):
    descripcion: str
    estado: str
    costo: float
    id_vehiculo: int
    id_mecanico: Optional[int] = None

class OrdenTrabajoActualizar(BaseModel):
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    costo: Optional[float] = None
    id_vehiculo: Optional[int] = None
    id_mecanico: Optional[int] = None

class OrdenTrabajoRespuesta(BaseModel):
    id: int
    descripcion: str
    estado: str
    costo: float
    id_vehiculo: int
    id_mecanico: Optional[int] = None

    class Config:
        from_attributes = True