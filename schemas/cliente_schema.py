import re
from pydantic import BaseModel, field_validator
from typing import Optional

class ClienteCrear(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str

    @field_validator("email")
    @classmethod
    def validar_email(cls, valor):
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ValueError("El email no tiene un formato válido (ej: nomb@dominio.com)")
        return valor

class ClienteActualizar(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validar_email(cls, valor):
        if valor is not None and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ValueError("El email no tiene un formato válido (ej: nomb@dominio.com)")
        return valor

class ClienteRespuesta(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    telefono: str

    class Config:
        from_attributes = True