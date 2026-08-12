Proyecto de Gestión de Taller Automotriz
Este sistema permite gestionar clientes, vehículos, mecánicos y órdenes de trabajo para un taller mecánico.

Requisitos previos
Para ejecutar este proyecto, asegúrate de tener instalado en tu computadora:

Python (3.10 o superior)

Node.js (versión LTS)

PostgreSQL y pgAdmin 4

Configuración inicial
Clonar el repositorio:

Bash
git clone https://github.com/KevinVilchezM/AVANZE-API.git
cd AVANZEAPI

Base de Datos:

Crea una base de datos en pgAdmin llamada taller_autos_db.

Abre el archivo TABLA.md (ubicado en esta carpeta), copia el contenido y ejecútalo en el Query Tool de pgAdmin.

Instrucciones de ejecución
Backend (FastAPI)
Desde la raíz de la carpeta AVANZEAPI, abre una terminal y ejecuta:

Bash
# Instalar dependencias
python -m pip install psycopg2-binary  (instalar en la terminal)
python -m pip install pydantic (instalar en la terminal)
python -m pip install fastapi ( instalar en la terminal)
python -m pip install uvicorn (instalar uvicorn)


# Iniciar servidor (asegúrate de configurar tus variables de entorno DB_PASSWORD)
$env:DB_PASSWORD = "admin123"
uvicorn main:app --reload
Frontend (React)
Abre una nueva terminal y dirígete a la carpeta del frontend:

Bash
cd GestionDeTallerdeAutos

# Instalar dependencias
npm install

# Iniciar aplicación
npm run dev
La aplicación estará disponible en http://localhost:5173.