from fastapi import APIRouter, HTTPException, Depends
from app.core.database import users_collection
from app.schemas.user_schema import UserCreate, UserResponse
from app.core.security import hash_password
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    """Registra un nuevo usuario en la base de datos."""
    # Verificar si el usuario ya existe
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado")

    # Hashear la contraseña antes de almacenarla
    hashed_password = hash_password(user.password)
    print(f"Contraseña hasheada: {hashed_password}")  # Para depuración
    
    # Crear usuario en la base de datos
    user_data = user.dict()
    user_data["password"] = hashed_password  # Guardar la contraseña encriptada
    await users_collection.insert_one(user_data)

    return UserResponse(name=user.name, email=user.email)
