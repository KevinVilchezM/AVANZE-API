class OrdenTrabajo:
    def __init__(self, descripcion, estado, costo, id_vehiculo, id_mecanico=None):
        self.id = None
        self.descripcion = descripcion
        self.estado = estado
        self.costo = costo
        self.id_vehiculo = id_vehiculo
        self.id_mecanico = id_mecanico

    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "costo": self.costo,
            "id_vehiculo": self.id_vehiculo,
            "id_mecanico": self.id_mecanico
        }

    @classmethod
    def from_dict(cls, datos):
        ot = cls(datos["descripcion"], datos["estado"], datos["costo"], datos["id_vehiculo"], datos["id_mecanico"])
        ot.id = datos.get("id")
        return ot

    def __str__(self):
        mecanico_str = f"Mecánico ID: {self.id_mecanico}" if self.id_mecanico else "Sin asignar"
        return f"[{self.id}] Vehículo ID: {self.id_vehiculo} | {self.descripcion} | {self.estado} | Costo: S/. {self.costo} | {mecanico_str}"