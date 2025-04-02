from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(title="MyMind - User Service")

# Conexión a MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("mymind_users")  # Nombre de la BD

# Importar y registrar las rutas
from app.routes import users, audio, transcriptions

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(audio.router, prefix="/audio", tags=["Audio"])
app.include_router(transcriptions.router, prefix="/users/transcriptions", tags=["Transcriptions"])

# Ruta de prueba
@app.get("/")
async def root():
    return {"message": "Bienvenido al servicio de usuarios de MyMind 🚀"}

