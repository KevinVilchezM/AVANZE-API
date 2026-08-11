from fastapi import APIRouter, HTTPException
from dao.cliente_dao import ClienteDAO, ClienteNoEncontradoError
from modelos.cliente import Cliente
from schemas.cliente_schema import ClienteCrear, ClienteActualizar, ClienteRespuesta

router = APIRouter(prefix="/clientes", tags=["Clientes"])
dao = ClienteDAO()

@router.get("/", response_model=list[ClienteRespuesta])
def listar_clientes():
    return [c.to_dict() for c in dao.obtener_todos()]

@router.get("/{cliente_id}", response_model=ClienteRespuesta)
def obtener_cliente(cliente_id: int):
    c = dao.buscar_por_id(cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Cliente ID={cliente_id} no encontrado")
    return c.to_dict()

@router.post("/", response_model=ClienteRespuesta, status_code=201)
def crear_cliente(datos: ClienteCrear):
    c = dao.insertar(Cliente(datos.nombre, datos.apellido, datos.telefono, datos.email))
    return c.to_dict()
    
@router.put("/{cliente_id}", response_model=ClienteRespuesta)
def actualizar_cliente(cliente_id: int, datos: ClienteActualizar):
    try:
        c = dao.actualizar(cliente_id, datos.nombre, datos.apellido, datos.telefono, datos.email)
        return c.to_dict()
    except ClienteNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    
@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    try:
        dao.eliminar(cliente_id)
        return {"mensaje": f"Cliente ID={cliente_id} eliminado"}
    except ClienteNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))