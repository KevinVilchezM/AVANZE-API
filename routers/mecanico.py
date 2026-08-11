from fastapi import APIRouter, HTTPException
from dao.mecanico_dao import MecanicoDAO, MecanicoNoEncontradoError
from modelos.mecanico import Mecanico
from schemas.mecanico_schema import MecanicoCrear, MecanicoActualizar, MecanicoRespuesta

router = APIRouter(prefix="/mecanicos", tags=["Mecánicos"])
dao = MecanicoDAO()

@router.get("/", response_model=list[MecanicoRespuesta])
def listar_mecanicos():
    return [m.to_dict() for m in dao.obtener_todos()]

@router.get("/{mecanico_id}", response_model=MecanicoRespuesta)
def obtener_mecanico(mecanico_id: int):
    m = dao.buscar_por_id(mecanico_id)
    if not m:
        raise HTTPException(status_code=404, detail=f"Mecánico ID={mecanico_id} no encontrado")
    return m.to_dict()

@router.post("/", response_model=MecanicoRespuesta, status_code=201)
def crear_mecanico(datos: MecanicoCrear):
    m = dao.insertar(Mecanico(datos.nombre, datos.apellido, datos.especialidad))
    return m.to_dict()

@router.put("/{mecanico_id}", response_model=MecanicoRespuesta)
def actualizar_mecanico(mecanico_id: int, datos: MecanicoActualizar):
    try:
        m = dao.actualizar(mecanico_id, datos.nombre, datos.apellido, datos.especialidad)
        return m.to_dict()
    except MecanicoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{mecanico_id}")
def eliminar_mecanico(mecanico_id: int):
    try:
        dao.eliminar(mecanico_id)
        return {"mensaje": f"Mecánico ID={mecanico_id} eliminado"}
    except MecanicoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))