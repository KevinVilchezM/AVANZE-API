class Cliente:
    def __init__(self, nombre, apellido, telefono, email):
        self.id = None
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, datos):
        c = cls(datos["nombre"], datos["apellido"], datos["telefono"], datos["email"])
        c.id = datos.get("id")
        return c

    def __str__(self):
        return f"[{self.id}] {self.apellido}, {self.nombre} | {self.telefono} | {self.email}"