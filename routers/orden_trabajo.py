from fastapi import APIRouter, HTTPException
from dao.orden_trabajo_dao import OrdenTrabajoDAO, OrdenTrabajoNoEncontradaError
from modelos.orden_trabajo import OrdenTrabajo
from schemas.orden_trabajo_schema import OrdenTrabajoCrear, OrdenTrabajoActualizar, OrdenTrabajoRespuesta

router = APIRouter(prefix="/ordenes", tags=["Órdenes de Trabajo"])
dao = OrdenTrabajoDAO()

@router.get("/", response_model=list[OrdenTrabajoRespuesta])
def listar_ordenes():
    return [ot.to_dict() for ot in dao.obtener_todos()]

@router.get("/{orden_id}", response_model=OrdenTrabajoRespuesta)
def obtener_orden(orden_id: int):
    ot = dao.buscar_por_id(orden_id)
    if not ot:
        raise HTTPException(status_code=404, detail=f"Orden de trabajo ID={orden_id} no encontrada")
    return ot.to_dict()

@router.post("/", response_model=OrdenTrabajoRespuesta, status_code=201)
def crear_orden(datos: OrdenTrabajoCrear):
    ot = dao.insertar(OrdenTrabajo(datos.descripcion, datos.estado, datos.costo, datos.id_vehiculo, datos.id_mecanico))
    return ot.to_dict()

@router.put("/{orden_id}", response_model=OrdenTrabajoRespuesta)
def actualizar_orden(orden_id: int, datos: OrdenTrabajoActualizar):
    try:
        ot = dao.actualizar(orden_id, datos.descripcion, datos.estado, datos.costo, datos.id_vehiculo, datos.id_mecanico)
        return ot.to_dict()
    except OrdenTrabajoNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{orden_id}")
def eliminar_orden(orden_id: int):
    try:
        dao.eliminar(orden_id)
        return {"mensaje": f"Orden de trabajo ID={orden_id} eliminada"}
    except OrdenTrabajoNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))