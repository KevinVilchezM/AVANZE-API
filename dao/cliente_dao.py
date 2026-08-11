import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.cliente import Cliente

# EXCEPCIONES
class ClienteNoEncontradoError(Exception):
    def __init__(self, cliente_id):
        super().__init__(f"Cliente ID={cliente_id} no encontrado")

class ClienteConVehiculosError(Exception):
    def __init__(self, cliente_id):
        super().__init__(f"Cliente ID={cliente_id} no se puede eliminar: tiene vehículos asociados")

# CLASE CLIENTE DAO
class ClienteDAO:
    def __init__(self):
        self.__log = Logger()

    # MAPEO DE FILA A OBJETO
    def __fila_a_cliente(self, fila):
        # Al usar RealDictCursor, fila ya es un diccionario
        c = Cliente(fila["nombre"], fila["apellido"], fila["telefono"], fila["email"])
        c.id = fila["id"]
        return c

    # BUSCAR POR ID
    def buscar_por_id(self, cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, apellido, telefono, email FROM clientes WHERE id = %s", (cliente_id,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return self.__fila_a_cliente(fila) if fila else None

    # INSERTAR
    def insertar(self, cliente):
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            # Usamos %s para Postgres y RETURNING id para obtener el ID autogenerado
            cursor.execute(
                "INSERT INTO clientes (nombre, apellido, telefono, email) VALUES (%s, %s, %s, %s) RETURNING id",
                (cliente.nombre, cliente.apellido, cliente.telefono, cliente.email)
            )
            cliente.id = cursor.fetchone()["id"]
            conn.commit()
            self.__log.info(f"Cliente agregado: {cliente.nombre} {cliente.apellido} (ID={cliente.id})")
            return cliente
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    # OBTENER TODOS
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, apellido, telefono, email FROM clientes ORDER BY apellido, nombre")
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [self.__fila_a_cliente(f) for f in filas]

    # ACTUALIZAR
    def actualizar(self, cliente_id, nombre=None, apellido=None, telefono=None, email=None):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self.__log.error(f"Actualizar fallido: Cliente ID={cliente_id} no existe")
            raise ClienteNoEncontradoError(cliente_id)

        nuevo_nombre = nombre if nombre is not None else c.nombre
        nuevo_apellido = apellido if apellido is not None else c.apellido
        nuevo_telefono = telefono if telefono is not None else c.telefono
        nuevo_email = email if email is not None else c.email

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE clientes SET nombre = %s, apellido = %s, telefono = %s, email = %s WHERE id = %s",
                (nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_email, cliente_id)
            )
            conn.commit()
            self.__log.info(f"Cliente actualizado: ID={cliente_id}")
            c.nombre = nuevo_nombre
            c.apellido = nuevo_apellido
            c.telefono = nuevo_telefono
            c.email = nuevo_email
            return c
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    # ELIMINAR
    def eliminar(self, cliente_id):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self.__log.error(f"Eliminar fallido: Cliente ID={cliente_id} no existe")
            raise ClienteNoEncontradoError(cliente_id)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
            conn.commit()
            self.__log.info(f"Cliente eliminado: ID={cliente_id}")
        except psycopg2.IntegrityError:
            conn.rollback()
            self.__log.error(f"Eliminar fallido: Cliente ID={cliente_id} tiene vehículos asociados")
            raise ClienteConVehiculosError(cliente_id)
        finally:
            cursor.close()
            conn.close()

    # TOTAL
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM clientes")
        # Con RealDictCursor, accedemos por el alias 'total'
        total = cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total                       