import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.mecanico import Mecanico

# EXCEPCIONES
class MecanicoNoEncontradoError(Exception):
    def __init__(self, mecanico_id):
        super().__init__(f"Mecánico ID={mecanico_id} no encontrado")

class MecanicoConOrdenesError(Exception):
    def __init__(self, mecanico_id):
        super().__init__(f"Mecánico ID={mecanico_id} no se puede eliminar: tiene órdenes asociadas")

# CLASE MECANICO DAO
class MecanicoDAO:
    def __init__(self):
        self.__log = Logger()

    # MAPEO DE FILA A OBJETO
    def __fila_a_mecanico(self, fila):
        m = Mecanico(fila["nombre"], fila["apellido"], fila["especialidad"])
        m.id = fila["id"]
        return m

    # BUSCAR POR ID
    def buscar_por_id(self, mecanico_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nombre, apellido, especialidad FROM mecanico WHERE id = %s", (mecanico_id,))
            fila = cursor.fetchone()
            return self.__fila_a_mecanico(fila) if fila else None
        finally:
            cursor.close()
            conn.close()

    # INSERTAR
    def insertar(self, mecanico):
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO mecanico (nombre, apellido, especialidad) VALUES (%s, %s, %s) RETURNING id",
                (mecanico.nombre, mecanico.apellido, mecanico.especialidad)
            )
            mecanico.id = cursor.fetchone()["id"]
            conn.commit()
            self.__log.info(f"Mecánico agregado: {mecanico.nombre} {mecanico.apellido} (ID={mecanico.id})")
            return mecanico
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
        try:
            cursor.execute("SELECT id, nombre, apellido, especialidad FROM mecanico ORDER BY apellido, nombre")
            filas = cursor.fetchall()
            return [self.__fila_a_mecanico(f) for f in filas]
        finally:
            cursor.close()
            conn.close()

    # ACTUALIZAR
    def actualizar(self, mecanico_id, nombre=None, apellido=None, especialidad=None):
        m = self.buscar_por_id(mecanico_id)
        if not m:
            self.__log.error(f"Actualizar fallido: Mecánico ID={mecanico_id} no existe")
            raise MecanicoNoEncontradoError(mecanico_id)

        nuevo_nombre = nombre if nombre is not None else m.nombre
        nuevo_apellido = apellido if apellido is not None else m.apellido
        nueva_especialidad = especialidad if especialidad is not None else m.especialidad

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE mecanico SET nombre = %s, apellido = %s, especialidad = %s WHERE id = %s",
                (nuevo_nombre, nuevo_apellido, nueva_especialidad, mecanico_id)
            )
            conn.commit()
            self.__log.info(f"Mecánico actualizado: ID={mecanico_id}")
            m.nombre = nuevo_nombre
            m.apellido = nuevo_apellido
            m.especialidad = nueva_especialidad
            return m
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    # ELIMINAR
    def eliminar(self, mecanico_id):
        m = self.buscar_por_id(mecanico_id)
        if not m:
            self.__log.error(f"Eliminar fallido: Mecánico ID={mecanico_id} no existe")
            raise MecanicoNoEncontradoError(mecanico_id)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM mecanico WHERE id = %s", (mecanico_id,))
            conn.commit()
            self.__log.info(f"Mecánico eliminado: ID={mecanico_id}")
            return True
        except psycopg2.IntegrityError:
            conn.rollback()
            self.__log.error(f"Eliminar fallido: Mecánico ID={mecanico_id} tiene órdenes asociadas")
            raise MecanicoConOrdenesError(mecanico_id)
        finally:
            cursor.close()
            conn.close()

    # TOTAL
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) AS total FROM mecanico")
            total = cursor.fetchone()["total"]
            return total
        finally:
            cursor.close()
            conn.close()