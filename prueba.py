from config.base_datos import inicializar
from dao.cliente_dao import ClienteDAO
from dao.vehiculo_dao import VehiculoDAO
from dao.mecanico_dao import MecanicoDAO
from dao.orden_trabajo_dao import OrdenTrabajoDAO

inicializar()

print("--- CLIENTES ---")
for c in ClienteDAO().obtener_todos():
    print(c)

print("\n--- VEHÍCULOS ---")
for v in VehiculoDAO().obtener_todos():
    print(v)

print("\n--- MECÁNICOS ---")
for m in MecanicoDAO().obtener_todos():
    print(m)

print("\n--- ÓRDENES DE TRABAJO ---")
for ot in OrdenTrabajoDAO().obtener_todos():
    print(ot)