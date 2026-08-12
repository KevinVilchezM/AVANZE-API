import psycopg2
import psycopg2.errors
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.vehiculo import Vehiculo

# EXCEPCIONES
class VehiculoNoEncontradoError(Exception):
    def __init__(self, vehiculo_id):
        super().__init__(f"Vehículo ID={vehiculo_id} no encontrado")

class PlacaDuplicadaError(Exception):
    def __init__(self, placa):
        super().__init__(f"La placa '{placa}' ya se encuentra registrada")

class VehiculoConOrdenesError(Exception):
    def __init__(self, vehiculo_id):
        super().__init__(f"Vehículo ID={vehiculo_id} no se puede eliminar: tiene órdenes asociadas")

class ClienteNoExisteError(Exception):
    def __init__(self, mensaje="El cliente especificado no existe en la base de datos"):
        super().__init__(mensaje)
# CLASE VEHICULO DAO
class VehiculoDAO:
    def __init__(self):
        self.__log = Logger()

    # MAPEO DE FILA A OBJETO
    def __fila_a_vehiculo(self, fila):
        v = Vehiculo(
            fila["placa"],
            fila["marca"],
            fila["modelo"],
            fila["anio"],
            fila["id_cliente"]
        )
        v.id = fila["id"]
        return v

    # BUSCAR POR ID
    def buscar_por_id(self, vehiculo_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, placa, marca, modelo, anio, id_cliente FROM vehiculo WHERE id = %s", (vehiculo_id,))
            fila = cursor.fetchone()
            return self.__fila_a_vehiculo(fila) if fila else None
        finally:
            cursor.close()
            conn.close()

    # BUSCAR POR PLACA
    def buscar_por_placa(self, placa):
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, placa, marca, modelo, anio, id_cliente FROM vehiculo WHERE placa = %s", (placa,))
            fila = cursor.fetchone()
            return self.__fila_a_vehiculo(fila) if fila else None
        finally:
            cursor.close()
            conn.close()

    # INSERTAR
    def insertar(self, vehiculo):
        if self.buscar_por_placa(vehiculo.placa):
            self.__log.warning(f"Placa duplicada: {vehiculo.placa}")
            raise PlacaDuplicadaError(vehiculo.placa)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO vehiculo (placa, marca, modelo, anio, id_cliente) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (vehiculo.placa, vehiculo.marca, vehiculo.modelo, vehiculo.anio, vehiculo.id_cliente)
            )
            vehiculo.id = cursor.fetchone()["id"]
            conn.commit()
            self.__log.info(f"Vehículo agregado: {vehiculo.placa} (ID={vehiculo.id})")
            return vehiculo
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            self.__log.error(f"Error de integridad: El clienteID={vehiculo.id_cliente} no existe")
            raise ClienteNoExisteError(f"El cliente con ID {vehiculo.id_cliente} no se encuentra registrado.")
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
            cursor.execute("SELECT id, placa, marca, modelo, anio, id_cliente FROM vehiculo ORDER BY marca, modelo")
            filas = cursor.fetchall()
            return [self.__fila_a_vehiculo(f) for f in filas]
        finally:
            cursor.close()
            conn.close()

    # OBTENER POR CLIENTE
    def obtener_por_cliente(self, id_cliente):
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, placa, marca, modelo, anio, id_cliente FROM vehiculo WHERE id_cliente = %s", (id_cliente,))
            filas = cursor.fetchall()
            return [self.__fila_a_vehiculo(f) for f in filas]
        finally:
            cursor.close()
            conn.close()

    # ACTUALIZAR
    def actualizar(self, vehiculo_id, placa=None, marca=None, modelo=None, anio=None, id_cliente=None):
        v = self.buscar_por_id(vehiculo_id)
        if not v:
            self.__log.error(f"Actualizar fallido: Vehículo ID={vehiculo_id} no existe")
            raise VehiculoNoEncontradoError(vehiculo_id)

        nueva_placa = placa if placa is not None else v.placa
        nueva_marca = marca if marca is not None else v.marca
        nuevo_modelo = modelo if modelo is not None else v.modelo
        nuevo_anio = anio if anio is not None else v.anio
        nuevo_id_cliente = id_cliente if id_cliente is not None else v.id_cliente

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE vehiculo SET placa = %s, marca = %s, modelo = %s, anio = %s, id_cliente = %s WHERE id = %s",
                (nueva_placa, nueva_marca, nuevo_modelo, nuevo_anio, nuevo_id_cliente, vehiculo_id)
            )
            conn.commit()
            self.__log.info(f"Vehículo actualizado: ID={vehiculo_id}")
            v.placa = nueva_placa
            v.marca = nueva_marca
            v.modelo = nuevo_modelo
            v.anio = nuevo_anio
            v.id_cliente = nuevo_id_cliente
            return v
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            self.__log.error(f"Error de integridad al actualizar: El cliente ID={nuevo_id_cliente} no existe")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    # ELIMINAR
    def eliminar(self, vehiculo_id):
        v = self.buscar_por_id(vehiculo_id)
        if not v:
            self.__log.error(f"Eliminar fallido: Vehículo ID={vehiculo_id} no existe")
            raise VehiculoNoEncontradoError(vehiculo_id)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM vehiculo WHERE id = %s", (vehiculo_id,))
            conn.commit()
            self.__log.info(f"Vehículo eliminado: ID={vehiculo_id}")
            return True
        except psycopg2.IntegrityError:
            conn.rollback()
            self.__log.error(f"Eliminar fallido: Vehículo ID={vehiculo_id} tiene órdenes asociadas")
            raise VehiculoConOrdenesError(vehiculo_id)
        finally:
            cursor.close()
            conn.close()

    # TOTAL
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) AS total FROM vehiculo")
            return cursor.fetchone()["total"]
        finally:
            cursor.close()
            conn.close()