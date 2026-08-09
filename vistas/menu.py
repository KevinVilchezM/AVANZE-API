from modelos.cliente import Cliente
from dao.cliente_dao import ClienteNoEncontradoError
from modelos.vehiculo import Vehiculo
from dao.vehiculo_dao import PlacaDuplicadaError, VehiculoNoEncontradoError
from modelos.mecanico import Mecanico
from dao.mecanico_dao import MecanicoNoEncontradoError
from modelos.orden_trabajo import OrdenTrabajo
from dao.orden_trabajo_dao import OrdenTrabajoNoEncontradaError

def mostrar_menu(cfg):
    print(f"\n{'=' * 45}")
    print(f" {cfg.nombre} v{cfg.version}")
    print(f" {cfg.empresa}")
    print(f"{'=' * 45}")
    print(" 1. Agregar cliente")
    print(" 2. Agregar vehículo")
    print(" 3. Agregar mecánico")
    print(" 4. Crear orden de trabajo")
    print(" 5. Listar clientes")
    print(" 6. Listar vehículos")
    print(" 7. Listar mecánicos")
    print(" 8. Listar órdenes de trabajo")
    print(" 9. Actualizar cliente")
    print(" 10. Actualizar vehículo")
    print(" 11. Actualizar mecánico")
    print(" 12. Actualizar orden de trabajo")
    print(" 13. Eliminar cliente")
    print(" 14. Eliminar vehículo")
    print(" 15. Eliminar mecánico")
    print(" 16. Eliminar orden de trabajo")
    print(" 17. Show Historial de Logs")
    print(" 18. Limpiar Historial de Logs")
    print(" 0. Salir")
    print(f"{'=' * 45}")

def agregar_cliente(cdao):
    print("\n--- AGREGAR CLIENTE ---")
    nombre = input(" Nombre : ")
    apellido = input(" Apellido : ")
    telefono = input(" Teléfono : ")
    email = input(" Email : ")
    c = cdao.insertar(Cliente(nombre, apellido, telefono, email))
    print(f" OK Cliente agregado con ID={c.id}")

def listar_todocliente(cdao):
    print("\n--- CLIENTES ---")
    clientes = cdao.obtener_todos()
    if clientes:
        for c in clientes:
            print(f" {c}")
    else:
        print(" (No hay clientes registrados)")

def actualizar_cliente(cdao):
    print("\n--- ACTUALIZAR CLIENTE ---")
    try:
        cliente_id = int(input(" ID del cliente a actualizar: "))
        nombre = input(" Nuevo nombre (Enter para no cambiar): ").strip()
        apellido = input(" Nuevo apellido (Enter para no cambiar): ").strip()
        telefono = input(" Nuevo teléfono (Enter para no cambiar): ").strip()
        email = input(" Nuevo email (Enter para no cambiar): ").strip()
        c = cdao.actualizar(
            cliente_id, 
            nombre or None, 
            apellido or None, 
            telefono or None, 
            email or None
        )
        print(f" OK Cliente actualizado: {c}")
    except ClienteNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero")

def eliminar_cliente(cdao):
    print("\n--- ELIMINAR CLIENTE ---")
    try:
        cliente_id = int(input(" ID del cliente a eliminar: "))
        cdao.eliminar(cliente_id)
        print(f" OK Cliente ID={cliente_id} eliminado")
    except ClienteNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero")

def agregar_vehiculo(vdao, cdao):
    print("\n--- AGREGAR VEHÍCULO ---")
    placa = input(" Placa : ")
    marca = input(" Marca : ")
    modelo = input(" Modelo : ")
    try:
        anio = int(input(" Año : "))
        id_cliente = int(input(" ID del Cliente Propietario: "))
        
        if not cdao.buscar_por_id(id_cliente):
            print(f" ERROR: El Cliente con ID={id_cliente} no existe")
            return
        v = vdao.insertar(Vehiculo(placa, marca, modelo, anio, id_cliente))
        print(f" OK Vehículo agregado con ID={v.id}")
    except PlacaDuplicadaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El año y el ID de cliente deben ser números enteros")

def listar_todovehiculo(vdao):
    print("\n--- VEHÍCULOS ---")
    vehiculos = vdao.obtener_todos()
    if vehiculos:
        for v in vehiculos:
            print(f" {v}")
    else:
        print(" (No hay vehículos registrados)")

def actualizar_vehiculo(vdao):
    print("\n--- ACTUALIZAR VEHÍCULO ---")
    try:
        vehiculo_id = int(input(" ID del vehículo a actualizar: "))
        marca = input(" Nueva marca (Enter para no cambiar): ").strip()
        modelo = input(" Nuevo modelo (Enter para no cambiar): ").strip()
        anio_str = input(" Nuevo año (Enter para no cambiar): ").strip()
        anio = int(anio_str) if anio_str else None
        
        v = vdao.actualizar(vehiculo_id, marca or None, modelo or None, anio)
        print(f" OK Vehículo actualizado: {v}")
    except VehiculoNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: ID debe ser entero y año debe ser número entero")

def eliminar_vehiculo(vdao):
    print("\n--- ELIMINAR VEHÍCULO ---")
    try:
        vehiculo_id = int(input(" ID del vehículo a eliminar: "))
        vdao.eliminar(vehiculo_id)
        print(f" OK Vehículo ID={vehiculo_id} eliminado")
    except VehiculoNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero")

def agregar_mecanico(mdao):
    print("\n--- AGREGAR MECÁNICO ---")
    nombre = input(" Nombre : ")
    apellido = input(" Apellido : ")
    especialidad = input(" Especialidad : ")
    m = mdao.insertar(Mecanico(nombre, apellido, especialidad))
    print(f" OK Mecánico agregado con ID={m.id}")

def listar_todomecanico(mdao):
    print("\n--- MECÁNICOS ---")
    mecanicos = mdao.obtener_todos()
    if mecanicos:
        for m in mecanicos:
            print(f" {m}")
    else:
        print(" (No hay mecánicos registrados)")


def actualizar_mecanico(mdao):
    print("\n--- ACTUALIZAR MECÁNICO ---")
    try:
        mecanico_id = int(input(" ID del mecánico a actualizar: "))
        especialidad = input(" Nueva especialidad (Enter para no cambiar): ").strip()
        m = mdao.actualizar(mecanico_id, especialidad or None)
        print(f" OK Mecánico actualizado: {m}")
    except MecanicoNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero")


def eliminar_mecanico(mdao):
    print("\n--- ELIMINAR MECÁNICO ---")
    try:
        mecanico_id = int(input(" ID del mecánico a eliminar: "))
        mdao.eliminar(mecanico_id)
        print(f" OK Mecánico ID={mecanico_id} eliminado")
    except MecanicoNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero")


def agregar_orden(odao, vdao, mdao):
    print("\n--- CREAR ÓRDEN DE TRABAJO ---")
    try:
        id_vehiculo = int(input(" ID del Vehículo: "))
        if not vdao.buscar_por_id(id_vehiculo):
            print(f" ERROR: El Vehículo con ID={id_vehiculo} no existe")
            return

        descripcion = input(" Descripción de la falla: ")
        estado = input(" Estado inicial de la orden (pendiente/proceso/listo): ").strip().lower()
        costo = float(input(" Costo total estimado (S/.): "))
        mecanico_str = input(" ID del Mecánico asignado (Enter para asignar luego): ").strip()
        id_mecanico = int(mecanico_str) if mecanico_str else None

        if id_mecanico and not mdao.buscar_por_id(id_mecanico):
            print(f" ERROR: El Mecánico con ID={id_mecanico} no existe")
            return

        o = odao.insertar(OrdenTrabajo(descripcion, estado, costo, id_vehiculo, id_mecanico))
        print(f" OK Orden de trabajo agregada con ID={o.id}")
    except ValueError:
        print(" ERROR: El ID del vehículo/mecánico debe ser entero y el costo un número")

def listar_todoorden(odao):
    print("\n--- ÓRDENES DE TRABAJO ---")
    ordenes = odao.obtener_todos()
    if ordenes:
        for o in ordenes:
            print(f" {o}")
    else:
        print(" (No hay órdenes de trabajo registradas)")

def actualizar_orden(odao, mdao):
    print("\n--- ACTUALIZAR ÓRDEN DE TRABAJO ---")
    try:
        orden_id = int(input(" ID de la orden a actualizar: "))
        estado = input(" Nuevo estado (pendiente/proceso/listo) (Enter para no cambiar): ").strip().lower()
        
        costo_str = input(" Nuevo costo estimado (S/.) (Enter para no cambiar): ").strip()
        costo = float(costo_str) if costo_str else None

        mecanico_str = input(" Nuevo ID de Mecánico (Enter para no cambiar): ").strip()
        id_mecanico = int(mecanico_str) if mecanico_str else None

        if id_mecanico and not mdao.buscar_por_id(id_mecanico):
            print(f" ERROR: El Mecánico con ID={id_mecanico} no existe")
            return

        o = odao.actualizar(orden_id, estado or None, costo, id_mecanico)
        print(f" OK Orden actualizada: {o}")
    except OrdenTrabajoNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: Los IDs deben ser enteros y el costo un número")


def eliminar_orden(odao):
    print("\n--- ELIMINAR ÓRDEN DE TRABAJO ---")
    try:
        orden_id = int(input(" ID de la orden a eliminar: "))
        odao.eliminar(orden_id)
        print(f" OK Orden ID={orden_id} eliminada")
    except OrdenTrabajoNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero")