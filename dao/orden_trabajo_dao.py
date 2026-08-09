from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.orden_trabajo import OrdenTrabajo
import sqlite3

# EXCEPCIONES
class OrdenTrabajoNoEncontradaError(Exception):
    def __init__(self, orden_id):
        super().__init__(f"Orden de Trabajo ID={orden_id} no encontrada")

# CLASE ORDEN DE TRABAJO DAO
class OrdenTrabajoDAO:
    def __init__(self):
        self.__log = Logger()

    # MAPEO DE FILA A OBJETO
    def __fila_a_orden(self, fila):
        o = OrdenTrabajo(
            fila["descripcion"],
            fila["costo"],
            fila["id_mecanico"],
            fila["id_vehiculo"],
            fila["estado"]
        )
        o.id = fila["id"]
        return o

    # BUSCAR POR ID
    def buscar_por_id(self, orden_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, descripcion, estado, costo, id_mecanico, id_vehiculo FROM orden_trabajo WHERE id = ?", (orden_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_orden(fila) if fila else None

    # INSERTAR
    def insertar(self, orden):
        estado_inicial = getattr(orden, 'estado', 'Pendiente')

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orden_trabajo (descripcion, estado, costo, id_mecanico, id_vehiculo) VALUES (?, ?, ?, ?, ?)",
            (orden.descripcion, estado_inicial, orden.costo, orden.id_mecanico, orden.id_vehiculo)
        )
        conn.commit()
        orden.id = cursor.lastrowid
        conn.close()

        self.__log.info(f"Orden de Trabajo agregada: ID={orden.id}")
        return orden

    # OBTENER TODAS
    def obtener_todas(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, descripcion, estado, costo, id_mecanico, id_vehiculo FROM orden_trabajo ORDER BY id DESC")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_orden(f) for f in filas]

    # OBTENER POR ESTADO
    def obtener_por_estado(self, estado):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, descripcion, estado, costo, id_mecanico, id_vehiculo FROM orden_trabajo WHERE estado = ?", (estado,))
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_orden(f) for f in filas]

    # ACTUALIZAR
    def actualizar(self, orden_id, descripcion=None, estado=None, costo=None, id_mecanico=None, id_vehiculo=None):
        o = self.buscar_por_id(orden_id)
        if not o:
            self.__log.error(f"Actualizar fallido: Orden ID={orden_id} no existe")
            raise OrdenTrabajoNoEncontradaError(orden_id)

        nueva_descripcion = descripcion if descripcion is not None else o.descripcion
        nuevo_estado = estado if estado is not None else o.estado
        nuevo_costo = costo if costo is not None else o.costo
        nuevo_id_mecanico = id_mecanico if id_mecanico is not None else o.id_mecanico
        nuevo_id_vehiculo = id_vehiculo if id_vehiculo is not None else o.id_vehiculo

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orden_trabajo SET descripcion = ?, estado = ?, costo = ?, id_mecanico = ?, id_vehiculo = ? WHERE id = ?",
            (nueva_descripcion, nuevo_estado, nuevo_costo, nuevo_id_mecanico, nuevo_id_vehiculo, orden_id)
        )
        conn.commit()
        conn.close()

        self.__log.info(f"Orden de Trabajo actualizada: ID={orden_id}")
        o.descripcion = nueva_descripcion
        o.estado = nuevo_estado
        o.costo = nuevo_costo
        o.id_mecanico = nuevo_id_mecanico
        o.id_vehiculo = nuevo_id_vehiculo
        return o

    # ELIMINAR
    def eliminar(self, orden_id):
        o = self.buscar_por_id(orden_id)
        if not o:
            self.__log.error(f"Eliminar fallido: Orden ID={orden_id} no existe")
            raise OrdenTrabajoNoEncontradaError(orden_id)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orden_trabajo WHERE id = ?", (orden_id,))
        conn.commit()
        conn.close()
        self.__log.info(f"Orden de Trabajo eliminada: ID={orden_id}")
        return True

    # TOTAL
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orden_trabajo")
        total = cursor.fetchone()[0]
        conn.close()
        return total