from pydantic import BaseModel, field_validator
from typing import Optional

class MecanicoCrear(BaseModel):
    nombre: str
    apellido: str
    especialidad: str

class MecanicoActualizar(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    especialidad: Optional[str] = None

class MecanicoRespuesta(BaseModel):
    id: int
    nombre: str
    apellido: str
    especialidad: str

    class Config:
        from_attributes = True