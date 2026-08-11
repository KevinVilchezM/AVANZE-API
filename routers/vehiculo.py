from fastapi import APIRouter, HTTPException
from dao.vehiculo_dao import VehiculoDAO, VehiculoNoEncontradoError, PlacaDuplicadaError, VehiculoConOrdenesError
from modelos.vehiculo import Vehiculo
from schemas.vehiculo_schema import VehiculoCrear, VehiculoActualizar, VehiculoRespuesta

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])
dao = VehiculoDAO()

@router.get("/", response_model=list[VehiculoRespuesta])
def listar_vehiculos():
    return [v.to_dict() for v in dao.obtener_todos()]

@router.get("/{vehiculo_id}", response_model=VehiculoRespuesta)
def obtener_vehiculo(vehiculo_id: int):
    v = dao.buscar_por_id(vehiculo_id)
    if not v:
        raise HTTPException(status_code=404, detail=f"Vehículo ID={vehiculo_id} no encontrado")
    return v.to_dict()

@router.post("/", response_model=VehiculoRespuesta, status_code=201)
def crear_vehiculo(datos: VehiculoCrear):
    try:
        v = dao.insertar(Vehiculo(datos.placa, datos.marca, datos.modelo, datos.anio, datos.id_cliente))
        return v.to_dict()
    except PlacaDuplicadaError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.put("/{vehiculo_id}", response_model=VehiculoRespuesta)
def actualizar_vehiculo(vehiculo_id: int, datos: VehiculoActualizar):
    try:
        v = dao.actualizar(vehiculo_id, datos.placa, datos.marca, datos.modelo, datos.anio, datos.id_cliente)
        return v.to_dict()
    except VehiculoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{vehiculo_id}")
def eliminar_vehiculo(vehiculo_id: int):
    try:
        dao.eliminar(vehiculo_id)
        return {"mensaje": f"Vehículo ID={vehiculo_id} eliminado"}
    except VehiculoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except VehiculoConOrdenesError as ex:
        raise HTTPException(status_code=400, detail=str(ex))