from fastapi import APIRouter, HTTPException, Depends
from app.core.database import users_collection
from app.core.auth import get_current_user
from app.schemas.user_schema import UserSchema
from datetime import datetime

router = APIRouter()

# 🔹 Register a new user
@router.post("/register")
async def register_user(user: UserSchema, user_id: str = Depends(get_current_user)):
    """Registers a new user in the database using Auth0's sub as _id."""
    existing_user = await users_collection.find_one({"_id": user_id})

    if existing_user:
        raise HTTPException(status_code=409, detail="User is already registered")

    user_data = user.dict()
    user_data["_id"] = user_id  # Use Auth0's sub as MongoDB _id
    user_data["transcriptions"] = []  # Initialize empty list

    await users_collection.insert_one(user_data)
    return {"message": "User successfully registered", "id": user_id}

# 🔹 Get all user
@router.get("/profile")
async def get_user_profile(user_id: str = Depends(get_current_user)):
    """Retrieves all user information."""
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 🔹 Get user's name
@router.get("/name")
async def get_user_name(user_id: str = Depends(get_current_user)):
    """Retrieves only the user's name."""
    user = await users_collection.find_one({"_id": user_id}, {"name": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 🔹 Update user name
@router.patch("/update-name")
async def update_name(new_name: str, user_id: str = Depends(get_current_user)):
    """Updates the user's name."""
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"name": new_name}}  # Actualiza el nombre del usuario
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No changes made to name")

    return {"message": "Name updated"}


# 🔹 Get user's email
@router.get("/email")
async def get_user_email(user_id: str = Depends(get_current_user)):
    """Retrieves only the user's email."""
    user = await users_collection.find_one({"_id": user_id}, {"email": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 🔹 Actualizar el email del usuario
@router.patch("/update-email")
async def update_email(new_email: str, user_id: str = Depends(get_current_user)):
    """Updates the user's email."""
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"email": new_email}}  # Actualiza el email del usuario
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No changes made to email")

    return {"message": "Email updated"}

# 🔹 Get notification settings
@router.get("/notifications")
async def get_notifications(user_id: str = Depends(get_current_user)):
    """Retrieves the user's notification settings."""
    user = await users_collection.find_one({"_id": user_id}, {"notifications": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# 🔹 Actualizar las notificaciones del usuario
@router.patch("/update-notifications")
async def update_notifications(new_notifications: bool, user_id: str = Depends(get_current_user)):
    """Updates the user's notification settings."""
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"notifications": new_notifications}}  # Actualiza las configuraciones de notificación
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No changes made to notifications settings")

    return {"message": "Notification settings updated"}

# 🔹 Get profile picture
@router.get("/profile-pic")
async def get_profile_pic(user_id: str = Depends(get_current_user)):
    """Retrieves the user's profile picture URL."""
    user = await users_collection.find_one({"_id": user_id}, {"profilePic": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 🔹 Update profile picture
@router.patch("/profile-pic")
async def update_profile_pic(profile_pic: str, user_id: str = Depends(get_current_user)):
    """Updates the user's profile picture URL."""
    result = await users_collection.update_one({"_id": user_id}, {"$set": {"profilePic": profile_pic}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or no changes made")
    return {"message": "Profile picture updated"}

# 🔹 Get privacy settings
@router.get("/privacy")
async def get_privacy_settings(user_id: str = Depends(get_current_user)):
    """Retrieves the user's privacy settings."""
    user = await users_collection.find_one({"_id": user_id}, {"privacy": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 🔹 Update privacy settings
@router.patch("/privacy")
async def update_privacy_settings(user_id: str = Depends(get_current_user)):
    """Toggles the user's privacy setting for anonymized usage."""
    # Buscar al usuario en la base de datos
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Obtener el valor actual de la preferencia 'allow_anonimized_usage'
    current_privacy = user.get("privacy", {}).get("allow_anonimized_usage", False)

    # Cambiar el valor: si es True, lo cambia a False, y si es False, lo cambia a True
    new_privacy_value = not current_privacy

    # Actualizar la base de datos con el nuevo valor
    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"privacy.allow_anonimized_usage": new_privacy_value}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No changes made to privacy settings")

    return {"message": "Privacy settings updated", "allow_anonimized_usage": new_privacy_value}

# 🔹 Delete user account
@router.delete("/delete")
async def delete_user(user_id: str = Depends(get_current_user)):
    """Deletes the user's account and all data."""
    result = await users_collection.delete_one({"_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User successfully deleted"}
