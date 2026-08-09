class Mecanico:
    def __init__(self, nombre, apellido, especialidad):
        self.id = None
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "especialidad": self.especialidad
        }

    @classmethod
    def from_dict(cls, datos):
        m = cls(datos["nombre"], datos["apellido"], datos["especialidad"])
        m.id = datos.get("id")
        return m

    def __str__(self):
        return f"[{self.id}] {self.apellido}, {self.nombre} | Especialidad: {self.especialidad}"