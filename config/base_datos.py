import os
import psycopg2
from psycopg2.extras import RealDictCursor

def obtener_conexion():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "taller_autos_db"), 
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )
    
    # Esto asegura que los resultados sean diccionarios
    return conn

def inicializar():
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # 1. Tabla Mecánico (SERIAL para autoincremento en Postgres)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mecanico (
            id          SERIAL PRIMARY KEY,
            nombre      TEXT    NOT NULL,
            apellido    TEXT    NOT NULL,
            especialidad TEXT    NOT NULL
        )
    """)
    
    # 2. Tabla Clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id          SERIAL PRIMARY KEY,
            nombre      TEXT    NOT NULL,
            apellido    TEXT    NOT NULL,
            telefono    TEXT    NOT NULL,
            email       TEXT    NOT NULL
        )
    """)
    
    # 3. Tabla Vehículo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehiculo (
            id          SERIAL PRIMARY KEY,
            placa       TEXT    UNIQUE NOT NULL,
            marca       TEXT    NOT NULL,
            modelo      TEXT    NOT NULL,
            anio        INTEGER NOT NULL,
            id_cliente  INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id)
        )
    """)
    
    # 4. Tabla Orden de Trabajo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orden_trabajo (
            id          SERIAL PRIMARY KEY,
            descripcion TEXT    NOT NULL,
            estado      TEXT    DEFAULT 'Pendiente',
            costo       REAL    NOT NULL,
            id_mecanico INTEGER NOT NULL,
            id_vehiculo INTEGER NOT NULL,
            FOREIGN KEY (id_mecanico) REFERENCES mecanico(id),
            FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id)
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()                                