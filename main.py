from config.sistema_config import SistemaConfig
from config.logger import Logger
from dao.cliente_dao import ClienteDAO
from dao.vehiculo_dao import VehiculoDAO
from dao.mecanico_dao import MecanicoDAO
from dao.orden_trabajo_dao import OrdenTrabajoDAO
from vistas.menu import mostrar_menu,agregar_cliente, listar_todocliente, actualizar_cliente, eliminar_cliente,agregar_vehiculo, listar_todovehiculo, actualizar_vehiculo, eliminar_vehiculo,agregar_mecanico, listar_todomecanico, actualizar_mecanico, eliminar_mecanico,agregar_orden, listar_todoorden, actualizar_orden, eliminar_orden

def main():
    cfg = SistemaConfig()
    cdao = ClienteDAO()
    vdao = VehiculoDAO()
    mdao = MecanicoDAO()
    odao = OrdenTrabajoDAO()

    while True:
        mostrar_menu(cfg)
        opcion = input(" Elige una opción: ").strip()
        
        match opcion:
            case "1":
                agregar_cliente(cdao)
                
            case "2":
                agregar_vehiculo(vdao, cdao)
                
            case "3":
                agregar_mecanico(mdao)
                
            case "4":
                agregar_orden(odao, vdao, mdao)
                
            case "5":
                listar_todocliente(cdao)
            case "6":
                listar_todovehiculo(vdao)
            case "7":
                listar_todomecanico(mdao)
            case "8":
                listar_todoorden(odao)
            case "9":
                actualizar_cliente(cdao)
                
            case "10":
                actualizar_vehiculo(vdao)
                
            case "11":
                actualizar_mecanico(mdao)
                
            case "12":
                actualizar_orden(odao, mdao)
                
            case "13":
                eliminar_cliente(cdao)
                
            case "14":
                eliminar_vehiculo(vdao)
                
            case "15":
                eliminar_mecanico(mdao)
                
            case "16":
                eliminar_orden(odao)
                
            case "17":
                Logger().mostrar_logs()
            case "18":
                Logger().limpiar()
            case "0":
                Logger().info("Sistema cerrado por el usuario")
                print("\n Hasta luego.")
                break
            case _:
                print(" Opción no válida, elige entre 0 y 18")


if __name__ == "__main__":
    main()