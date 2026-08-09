from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.vehiculo import Vehiculo
import sqlite3

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
        cursor.execute("SELECT id, placa, marca, modelo, anio, id_cliente FROM vehiculo WHERE id = ?", (vehiculo_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_vehiculo(fila) if fila else None

    # BUSCAR POR PLACA
    def buscar_por_placa(self, placa):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, placa, marca, modelo, anio, id_cliente FROM vehiculo WHERE placa = ?", (placa,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_vehiculo(fila) if fila else None

    # INSERTAR
    def insertar(self, vehiculo):
        if self.buscar_por_placa(vehiculo.placa):
            self.__log.warning(f"Placa duplicada: {vehiculo.placa}")
            raise PlacaDuplicadaError(vehiculo.placa)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO vehiculo (placa, marca, modelo, anio, id_cliente) VALUES (?, ?, ?, ?, ?)",
            (vehiculo.placa, vehiculo.marca, vehiculo.modelo, vehiculo.anio, vehiculo.id_cliente)
        )
        conn.commit()
        vehiculo.id = cursor.lastrowid
        conn.close()

        self.__log.info(f"Vehículo agregado: {vehiculo.placa} (ID={vehiculo.id})")
        return vehiculo

    # OBTENER TODOS
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, placa, marca, modelo, anio, id_cliente FROM vehiculo ORDER BY marca, modelo")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_vehiculo(f) for f in filas]

    # OBTENER POR CLIENTE
    def obtener_por_cliente(self, id_cliente):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, placa, marca, modelo, anio, id_cliente FROM vehiculo WHERE id_cliente = ?", (id_cliente,))
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_vehiculo(f) for f in filas]

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
        cursor.execute(
            "UPDATE vehiculo SET placa = ?, marca = ?, modelo = ?, anio = ?, id_cliente = ? WHERE id = ?",
            (nueva_placa, nueva_marca, nuevo_modelo, nuevo_anio, nuevo_id_cliente, vehiculo_id)
        )
        conn.commit()
        conn.close()

        self.__log.info(f"Vehículo actualizado: ID={vehiculo_id}")
        v.placa = nueva_placa
        v.marca = nueva_marca
        v.modelo = nuevo_modelo
        v.anio = nuevo_anio
        v.id_cliente = nuevo_id_cliente
        return v

    # ELIMINAR
    def eliminar(self, vehiculo_id):
        v = self.buscar_por_id(vehiculo_id)
        if not v:
            self.__log.error(f"Eliminar fallido: Vehículo ID={vehiculo_id} no existe")
            raise VehiculoNoEncontradoError(vehiculo_id)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM vehiculo WHERE id = ?", (vehiculo_id,))
            conn.commit()
            conn.close()
            self.__log.info(f"Vehículo eliminado: ID={vehiculo_id}")
            return True
        except sqlite3.IntegrityError:
            conn.close()
            self.__log.error(f"Eliminar fallido: Vehículo ID={vehiculo_id} tiene órdenes asociadas")
            raise VehiculoConOrdenesError(vehiculo_id)

    # TOTAL
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vehiculo")
        total = cursor.fetchone()[0]
        conn.close()
        return total