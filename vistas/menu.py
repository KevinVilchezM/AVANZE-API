from modelos.cliente import Cliente
from modelos.vehiculo import Vehiculo
from modelos.mecanico import Mecanico
from modelos.orden_trabajo import OrdenTrabajo
from dao.cliente_dao import ClienteDAO, ClienteNoEncontradoError
from dao.vehiculo_dao import VehiculoDAO, VehiculoNoEncontradoError, PlacaDuplicadaError, VehiculoConOrdenesError
from dao.mecanico_dao import MecanicoDAO, MecanicoNoEncontradoError
from dao.orden_trabajo_dao import OrdenTrabajoDAO, OrdenTrabajoNoEncontradaError
import json

def mostrar_menu(cfg):
    print(f"\n{'=' * 45}")
    print(f" {cfg.nombre} v{cfg.version}")
    print(f" {cfg.empresa}")
    print(f"{'=' * 45}")
    print(" -- CLIENTES ---------------------")
    print(" 1. Agregar cliente")
    print(" 2. Listar clientes")
    print(" 3. Actualizar cliente")
    print(" 4. Eliminar cliente")
    print(" -- VEHÍCULOS --------------------")
    print(" 5. Agregar vehículo")
    print(" 6. Listar vehículos")
    print(" 7. Actualizar vehículo")
    print(" 8. Eliminar vehículo")
    print(" -- MECÁNICOS --------------------")
    print(" 9. Agregar mecánico")
    print(" 10. Listar mecánicos")
    print(" 11. Actualizar mecánico")
    print(" 12. Eliminar mecánico")
    print(" -- ÓRDENES DE TRABAJO -----------")
    print(" 13. Registrar orden de trabajo")
    print(" 14. Listar órdenes de trabajo")
    print(" 15. Actualizar orden de trabajo")
    print(" 16. Eliminar orden de trabajo")
    print(" -- JSON / LOGS ------------------")
    print(" 17. Ver clientes en JSON")
    print(" 18. Ver vehículos en JSON")
    print(" 19. Ver mecánicos en JSON")
    print(" 20. Ver órdenes en JSON")
    print(" 0. Salir")
    print(f"{'=' * 45}")

# --- CLIENTES ---
def agregar_cliente(cdao):
    print("\n--- AGREGAR CLIENTE ---")
    nombre   = input("  Nombre   : ").strip()
    apellido = input("  Apellido : ").strip()
    email    = input("  Email    : ").strip()
    telefono = input("  Telefono : ").strip()
    try:
        c = cdao.insertar(Cliente(nombre, apellido, telefono, email))
        print(f" OK Cliente agregado con ID: {c.id}")
    except Exception as ex:
        print(f" ERROR {ex}")

def listar_clientes(cdao):
    print("\n--- CLIENTES ---")
    clientes = cdao.obtener_todos()
    if clientes:
        for c in clientes: print(f" {c}")
    else:
        print(" (No hay clientes registrados.)")

def actualizar_cliente(cdao):
    print("\n--- ACTUALIZAR CLIENTE ---")
    listar_clientes(cdao)
    try:
        cliente_id = int(input("  ID del cliente a actualizar: "))
        nombre   = input("  Nuevo Nombre   (Enter para no cambiar): ").strip()
        apellido = input("  Nuevo Apellido (Enter para no cambiar): ").strip()
        email    = input("  Nuevo Email    (Enter para no cambiar): ").strip()
        telefono = input("  Nuevo Telefono (Enter para no cambiar): ").strip()
        c = cdao.actualizar(cliente_id, nombre or None, apellido or None, telefono or None, email or None)
        print(f" OK Cliente actualizado: {c}")
    except ClienteNoEncontradoError as ex:
        print(f" ERROR {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")

def eliminar_cliente(cdao):
    print("\n--- ELIMINAR CLIENTE ---")
    listar_clientes(cdao)
    try:
        cliente_id = int(input("  ID del cliente a eliminar: "))
        cdao.eliminar(cliente_id)
        print(f" OK Cliente con ID {cliente_id} eliminado.")
    except ClienteNoEncontradoError as ex:
        print(f" ERROR {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")

# --- VEHÍCULOS ---
def agregar_vehiculo(vdao, cdao):
    print("\n--- AGREGAR VEHÍCULO ---")
    listar_clientes(cdao)
    try:
        id_cliente = int(input("  ID del propietario (Cliente): "))
        placa  = input("  Placa  : ").strip()
        marca  = input("  Marca  : ").strip()
        modelo = input("  Modelo : ").strip()
        anio   = int(input("  Año    : "))
        v = vdao.insertar(Vehiculo(placa, marca, modelo, anio, id_cliente))
        print(f" OK Vehículo agregado con ID: {v.id}")
    except PlacaDuplicadaError as ex:
        print(f" ERROR {ex}")
    except ValueError:
        print(" ERROR: El ID de cliente y año deben ser números enteros.")

def listar_vehiculos(vdao):
    print("\n--- VEHÍCULOS ---")
    vehiculos = vdao.obtener_todos()
    if vehiculos:
        for v in vehiculos: print(f" {v}")
    else:
        print(" (No hay vehículos registrados.)")

def actualizar_vehiculo(vdao):
    print("\n--- ACTUALIZAR VEHÍCULO ---")
    listar_vehiculos(vdao)
    try:
        vehiculo_id = int(input("  ID del vehículo a actualizar: "))
        placa  = input("  Nueva Placa  (Enter para no cambiar): ").strip()
        marca  = input("  Nueva Marca  (Enter para no cambiar): ").strip()
        modelo = input("  Nuevo Modelo (Enter para no cambiar): ").strip()
        anio_str = input("  Nuevo Año    (Enter para no cambiar): ").strip()
        anio = int(anio_str) if anio_str else None
        v = vdao.actualizar(vehiculo_id, placa or None, marca or None, modelo or None, anio)
        print(f" OK Vehículo actualizado: {v}")
    except VehiculoNoEncontradoError as ex:
        print(f" ERROR {ex}")
    except PlacaDuplicadaError as ex:
        print(f" ERROR {ex}")
    except ValueError:
        print(" ERROR: ID y año deben ser números enteros.")

def eliminar_vehiculo(vdao):
    print("\n--- ELIMINAR VEHÍCULO ---")
    listar_vehiculos(vdao)
    try:
        vehiculo_id = int(input("  ID del vehículo a eliminar: "))
        vdao.eliminar(vehiculo_id)
        print(f" OK Vehículo ID={vehiculo_id} eliminado.")
    except VehiculoNoEncontradoError as ex:
        print(f" ERROR {ex}")
    except VehiculoConOrdenesError as ex:
        print(f" ERROR {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")

# --- MECÁNICOS ---
def agregar_mecanico(mdao):
    print("\n--- AGREGAR MECÁNICO ---")
    nombre       = input("  Nombre       : ").strip()
    apellido     = input("  Apellido     : ").strip()
    especialidad = input("  Especialidad : ").strip()
    m = mdao.insertar(Mecanico(nombre, apellido, especialidad))
    print(f" OK Mecánico agregado con ID: {m.id}")

def listar_mecanicos(mdao):
    print("\n--- MECÁNICOS ---")
    mecanicos = mdao.obtener_todos()
    if mecanicos:
        for m in mecanicos: print(f" {m}")
    else:
        print(" (No hay mecánicos registrados.)")

def actualizar_mecanico(mdao):
    print("\n--- ACTUALIZAR MECÁNICO ---")
    listar_mecanicos(mdao)
    try:
        mecanico_id = int(input("  ID del mecánico a actualizar: "))
        nombre       = input("  Nuevo Nombre       (Enter para no cambiar): ").strip()
        apellido     = input("  Nuevo Apellido     (Enter para no cambiar): ").strip()
        especialidad = input("  Nueva Especialidad (Enter para no cambiar): ").strip()
        m = mdao.actualizar(mecanico_id, nombre or None, apellido or None, especialidad or None)
        print(f" OK Mecánico actualizado: {m}")
    except MecanicoNoEncontradoError as ex:
        print(f" ERROR {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")

def eliminar_mecanico(mdao):
    print("\n--- ELIMINAR MECÁNICO ---")
    listar_mecanicos(mdao)
    try:
        mecanico_id = int(input("  ID del mecánico a eliminar: "))
        mdao.eliminar(mecanico_id)
        print(f" OK Mecánico ID={mecanico_id} eliminado.")
    except MecanicoNoEncontradoError as ex:
        print(f" ERROR {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")

# --- ÓRDENES DE TRABAJO ---
def registrar_orden(odao, vdao, mdao):
    print("\n--- REGISTRAR ORDEN DE TRABAJO ---")
    listar_vehiculos(vdao)
    listar_mecanicos(mdao)
    try:
        id_vehiculo = int(input("  ID del vehículo : "))
        id_mecanico_str = input("  ID del mecánico (Enter si no asignado): ").strip()
        id_mecanico = int(id_mecanico_str) if id_mecanico_str else None
        descripcion = input("  Descripción     : ").strip()
        estado      = input("  Estado (Pendiente/En Proceso/Completado): ").strip()
        costo       = float(input("  Costo S/.       : "))
        
        if costo < 0:
            print(" ERROR: El costo no puede ser negativo.")
            return

        ot = odao.insertar(OrdenTrabajo(descripcion, estado, costo, id_vehiculo, id_mecanico))
        print(f" OK Orden de trabajo registrada con ID: {ot.id}")
    except ValueError:
        print(" ERROR: Los IDs deben ser enteros y el costo un número válido.")

def listar_ordenes(odao):
    print("\n--- ÓRDENES DE TRABAJO ---")
    ordenes = odao.obtener_todos()
    if ordenes:
        for ot in ordenes:
            print(f" {ot}")
    else:
        print(" (No hay órdenes de trabajo registradas)")

def actualizar_orden(odao):
    print("\n--- ACTUALIZAR ORDEN DE TRABAJO ---")
    listar_ordenes(odao)
    try:
        orden_id = int(input("  ID de la orden a actualizar: "))
        descripcion = input("  Nueva Descripción (Enter para no cambiar): ").strip()
        estado      = input("  Nuevo Estado      (Enter para no cambiar): ").strip()
        costo_str   = input("  Nuevo Costo       (Enter para no cambiar): ").strip()
        costo = float(costo_str) if costo_str else None
        
        ot = odao.actualizar(orden_id, descripcion or None, estado or None, costo)
        print(f" OK Orden actualizada: {ot}")
    except OrdenTrabajoNoEncontradaError as ex:
        print(f" ERROR {ex}")
    except ValueError:
        print(" ERROR: ID debe ser entero y costo un número válido.")

def eliminar_orden(odao):
    print("\n--- ELIMINAR ORDEN DE TRABAJO ---")
    listar_ordenes(odao)
    try:
        orden_id = int(input("  ID de la orden a eliminar: "))
        odao.eliminar(orden_id)
        print(f" OK Orden ID={orden_id} eliminada.")
    except OrdenTrabajoNoEncontradaError as ex:
        print(f" ERROR {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")

# --- JSON ---
def ver_clientes_json(cdao):
    print("\n--- CLIENTES EN JSON ---")
    clientes = cdao.obtener_todos()
    if clientes:
        datos = [c.to_dict() for c in clientes]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(" (No hay clientes registrados.)")

def ver_vehiculos_json(vdao):
    print("\n--- VEHÍCULOS EN JSON ---")
    vehiculos = vdao.obtener_todos()
    if vehiculos:
        datos = [v.to_dict() for v in vehiculos]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(" (No hay vehículos registrados.)")

def ver_mecanicos_json(mdao):
    print("\n--- MECÁNICOS EN JSON ---")
    mecanicos = mdao.obtener_todos()
    if mecanicos:
        datos = [m.to_dict() for m in mecanicos]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(" (No hay mecánicos registrados.)")

def ver_ordenes_json(odao):
    print("\n--- ÓRDENES EN JSON ---")
    ordenes = odao.obtener_todos()
    if ordenes:
        datos = [ot.to_dict() for ot in ordenes]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(" (No hay órdenes registradas.)")