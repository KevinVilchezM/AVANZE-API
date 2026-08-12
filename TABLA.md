-- 1. Crear la tabla Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(150)
);

-- 2. Crear la tabla Vehículos
CREATE TABLE IF NOT EXISTS vehiculo (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(15) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    anio INT NOT NULL,
    id_cliente INT NOT NULL REFERENCES clientes(id)
);

-- 3. Crear la tabla Mecánico
CREATE TABLE IF NOT EXISTS mecanico (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100)
);

-- 4. Crear la tabla Orden de Trabajo
CREATE TABLE IF NOT EXISTS orden_trabajo (
    id SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    estado VARCHAR(30) NOT NULL,
    costo REAL NOT NULL,
    id_mecanico INT NOT NULL REFERENCES mecanico(id),
    id_vehiculo INT NOT NULL REFERENCES vehiculo(id)
);

-- Insertar datos de prueba en Clientes
INSERT INTO clientes (nombre, apellido, telefono, email) VALUES 
('Juan', 'Perez', '987654321', 'juan.perez@email.com'),
('Maria', 'Garcia', '912345678', 'maria.garcia@email.com'),
('Luis', 'Mendoza', '955443322', 'luis.mendoza@email.com'),
('Ana', 'Torres', '966778899', 'ana.torres@email.com');

-- Insertar datos de prueba en Vehículos
INSERT INTO vehiculo (placa, marca, modelo, anio, id_cliente) VALUES 
('abc-123', 'toyota', 'corolla', 2020, 1),
('xyz-789', 'hyundai', 'tucson', 2018, 2),
('mno-456', 'kia', 'rio', 2021, 3),
('fgh-987', 'nissan', 'sentra', 2019, 4);

-- Insertar datos de prueba en Mecánicos
INSERT INTO mecanico (nombre, apellido, especialidad) VALUES 
('Carlos', 'Mendoza', 'frenos'),
('Luis', 'Gomez', 'electricidad'),
('Jorge', 'Ramos', 'alineamiento'),
('Ricardo', 'Silva', 'pintura');

-- Insertar datos de prueba en Órdenes de Trabajo
INSERT INTO orden_trabajo (descripcion, estado, costo, id_mecanico, id_vehiculo) VALUES 
('cambio de pastillas de freno', 'en proceso', 150.00, 1, 1),
('falla de luces', 'pendiente', 0.00, 2, 2),
('alineamiento de ruedas', 'terminado', 120.00, 3, 3),