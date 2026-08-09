import sqlite3

ARCHIVO_BD = "sistema.db"

def obtener_conexion():
    # sqlite3.connect() abre (o crea si no existe) el archivo de base de datos
    conn = sqlite3.connect(ARCHIVO_BD)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def inicializar():
    # crea tablas si aun no existen. Se llama UNA vez al iniciar el sistema.
    conn = obtener_conexion()
    cursor = conn.cursor()

    # 1. Tabla Mecánico
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mecanico(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            especialidad TEXT NOT NULL
        )
    """)

    # 2. Tabla Clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # 3. Tabla Vehículo (debe ir antes de orden_trabajo por la clave foránea)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehiculo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT UNIQUE NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            anio INTEGER NOT NULL,
            id_cliente INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id)
        )
    """)

    # 4. Tabla Orden de Trabajo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orden_trabajo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            estado TEXT DEFAULT 'Pendiente',
            costo REAL NOT NULL,
            id_mecanico INTEGER NOT NULL,
            id_vehiculo INTEGER NOT NULL,
            FOREIGN KEY (id_mecanico) REFERENCES mecanico(id),
            FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id)
        )
    """)

    conn.commit()
    conn.close()