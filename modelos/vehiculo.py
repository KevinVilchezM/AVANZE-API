class Vehiculo:
    def __init__(self, placa, marca, modelo, anio, id_cliente):
        self.id = None
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.id_cliente = id_cliente

    def to_dict(self):
        return {
            "id": self.id,
            "placa": self.placa,
            "marca": self.marca,
            "modelo": self.modelo,
            "anio": self.anio,
            "id_cliente": self.id_cliente
        }

    @classmethod
    def from_dict(cls, datos):
        v = cls(datos["placa"], datos["marca"], datos["modelo"], datos["anio"], datos["id_cliente"])
        v.id = datos.get("id")
        return v

    def __str__(self):
        return f"[{self.id}] Placa: {self.placa} | {self.marca} {self.modelo} ({self.anio}) | Cliente ID: {self.id_cliente}"