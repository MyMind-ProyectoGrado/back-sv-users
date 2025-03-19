from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """Esquema para recibir datos de registro de usuario."""
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Esquema de respuesta para cuando se registre un usuario."""
    name: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str