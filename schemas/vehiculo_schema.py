from pydantic import BaseModel, field_validator
from typing import Optional

class VehiculoCrear(BaseModel):
    placa: str
    marca: str
    modelo: str
    anio: int
    id_cliente: int

class VehiculoActualizar(BaseModel):
    placa: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    anio: Optional[int] = None
    id_cliente: Optional[int] = None

class VehiculoRespuesta(BaseModel):
    id: int
    placa: str
    marca: str
    modelo: str
    anio: int
    id_cliente: int

    class Config:
        from_attributes = True       