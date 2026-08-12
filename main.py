from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.base_datos import inicializar
from routers import cliente, vehiculo, mecanico, orden_trabajo


app = FastAPI(
    title="Sistema de Gestión de Taller de Autos",
    version="1.0",
    description="API REST para gestión de clientes, vehículos, mecánicos y órdenes de trabajo",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

inicializar()

app.include_router(cliente.router)
app.include_router(vehiculo.router)
app.include_router(mecanico.router)
app.include_router(orden_trabajo.router)

@app.get("/")
def inicio():
    return {
        "mensaje": "API Sistema de Gestión de Taller de Autos",
        "version": "1.0",
        "docs": "/docs",
    }