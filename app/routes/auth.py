from fastapi import APIRouter, HTTPException, Depends
from app.core.database import users_collection
from app.schemas.user_schema import UserLogin, TokenResponse
from app.core.security import (
    verify_password, create_access_token, create_refresh_token, decode_token
)
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Modelo para recibir el Refresh Token
class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/auth/login", response_model=TokenResponse)
async def login(user: UserLogin):
    """Inicia sesión y genera tokens JWT (access y refresh)."""

    # Buscar usuario en la base de datos
    existing_user = await users_collection.find_one({"email": user.email})
    if not existing_user:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    # Verificar contraseña
    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    # Generar tokens
    access_expiration = datetime.timedelta(hours=1)  # Access token dura 1 hora
    refresh_expiration = datetime.timedelta(days=7)  # Refresh token dura 7 días

    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_expiration)
    refresh_token = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_expiration)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """Renueva el Access Token usando un Refresh Token válido."""
    
    payload = decode_token(request.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Refresh token inválido o expirado")

    # Validar que realmente sea un refresh token (agrega un claim "type" cuando lo generes)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="El token proporcionado no es un refresh token")

    # Generar un nuevo access token y refresh token
    new_access_token = create_access_token({"sub": payload["sub"]})
    new_refresh_token = create_refresh_token({"sub": payload["sub"]})  # Renueva el refresh token también

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
