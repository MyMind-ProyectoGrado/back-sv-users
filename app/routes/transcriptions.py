from fastapi import APIRouter, HTTPException, Depends
from app.core.database import users_collection
from app.core.auth import get_current_user
from typing import Optional
from datetime import datetime
from bson import ObjectId
from fastapi import Query

router = APIRouter()

# 🔹 Obtener todas las transcripciones
@router.get("/")
async def get_all_transcriptions(user_id: str = Depends(get_current_user)):
    """Retrieves all transcriptions of the authenticated user."""
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user["transcriptions"]

# 🔹 Obtener transcripción específica por ID
@router.get("/{transcription_id}")
async def get_transcription_by_id(transcription_id: str, user_id: str = Depends(get_current_user)):
    """Retrieves a specific transcription by its ID."""
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transcription = next((t for t in user["transcriptions"] if t["_id"] == transcription_id), None)
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcription not found")

    return transcription

# 🔹 Obtener transcripciones por emoción
@router.get("/by-emotion/{emotion}")
async def get_transcriptions_by_emotion(emotion: str, user_id: str = Depends(get_current_user)):
    """Retrieves transcriptions filtered by emotion."""
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return [t for t in user["transcriptions"] if t.get("emotion") == emotion]

# 🔹 Obtener transcripciones por sentimiento
@router.get("/by-sentiment/{sentiment}")
async def get_transcriptions_by_sentiment(sentiment: str, user_id: str = Depends(get_current_user)):
    """Retrieves transcriptions filtered by sentiment."""
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return [t for t in user["transcriptions"] if t.get("sentiment") == sentiment]

# 🔹 Obtener transcripciones por tema
@router.get("/by-topic/{topic}")
async def get_transcriptions_by_topic(topic: str, user_id: str = Depends(get_current_user)):
    """Retrieves transcriptions filtered by topic."""
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return [t for t in user["transcriptions"] if t.get("topic") == topic]

# 🔹 Obtener transcripciones por fecha
@router.get("/by-date/{date}")
async def get_transcriptions_by_date(date: str, user_id: str = Depends(get_current_user)):
    """Retrieves transcriptions from a specific date (YYYY-MM-DD)."""
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return [t for t in user["transcriptions"] if t.get("date", "").startswith(date)]

# 🔹 Obtener transcripciones por hora o rango de horas
@router.get("/by-hour/")
async def get_transcriptions_by_hour(
    start_hour: int, 
    end_hour: Optional[int] = None,
    user_id: str = Depends(get_current_user)
):
    """Retrieves transcriptions from a specific hour or a range of hours."""
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transcriptions = user["transcriptions"]

    if end_hour is None:  # Solo una hora específica
        return [t for t in transcriptions if int(t.get("time", "00:00").split(":")[0]) == start_hour]
    else:  # Rango de horas
        return [t for t in transcriptions if start_hour <= int(t.get("time", "00:00").split(":")[0]) <= end_hour]

@router.get("/filter")
async def get_transcriptions_with_filters(
    emotion: Optional[str] = None,
    sentiment: Optional[str] = None,
    topic: Optional[str] = None,
    date: Optional[str] = None,
    start_hour: Optional[int] = Query(None, ge=0, le=23),  # Rango válido: 0-23
    end_hour: Optional[int] = Query(None, ge=0, le=23),
    user_id: str = Depends(get_current_user),
):
    """Retrieves transcriptions with optional filters for emotion, sentiment, topic, date, and hour range."""
    
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transcriptions = user["transcriptions"]

    # Aplicar filtros si se proporcionan
    if emotion:
        transcriptions = [t for t in transcriptions if t.get("emotion") == emotion]
    if sentiment:
        transcriptions = [t for t in transcriptions if t.get("sentiment") == sentiment]
    if topic:
        transcriptions = [t for t in transcriptions if t.get("topic") == topic]
    if date:
        transcriptions = [t for t in transcriptions if t.get("date", "").startswith(date)]
    
    # Filtrar por rango de horas
    if start_hour is not None and end_hour is not None:
        transcriptions = [
            t for t in transcriptions
            if start_hour <= int(t.get("time", "00:00").split(":")[0]) <= end_hour
        ]

    return transcriptions

# 🔹 Insertar una nueva transcripción
@router.post("/add-transcription")
async def add_transcription(
    transcription: dict,  # Esto debe ser un diccionario que incluya los campos: fecha, hora, texto, emoción, sentimiento, tema
    user_id: str = Depends(get_current_user)
):
    """Agrega una nueva transcripción al perfil del usuario."""
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Asegurarse de que la transcripción tenga los campos necesarios
    required_fields = ["fecha", "hora", "texto", "emocion", "sentimiento", "tema"]
    if not all(field in transcription for field in required_fields):
        raise HTTPException(status_code=400, detail="Missing required transcription fields")

    # Agregar la nueva transcripción al array de transcripciones del usuario
    transcription_data = {
        "_id": str(ObjectId()),  # Generar un nuevo ObjectId para la transcripción
        "fecha": transcription["fecha"],
        "hora": transcription["hora"],
        "texto": transcription["texto"],
        "emocion": transcription["emocion"],
        "sentimiento": transcription["sentimiento"],
        "tema": transcription["tema"]
    }

    # Añadir la transcripción a la base de datos
    result = await users_collection.update_one(
        {"_id": user_id},
        {"$push": {"transcripciones": transcription_data}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Failed to add transcription")

    return {"message": "Transcription added successfully", "transcription_id": transcription_data["_id"]}

# 🔹 Borrar transcripción por ID
@router.delete("/delete-transcription/{transcription_id}")
async def delete_transcription_by_id(transcription_id: str, user_id: str = Depends(get_current_user)):
    """Deletes a specific transcription by its ID."""
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Buscar la transcripción específica por ID
    result = await users_collection.update_one(
        {"_id": user_id},
        {"$pull": {"transcriptions": {"_id": transcription_id}}}  # Elimina la transcripción con ese ID
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Transcription not found")

    return {"message": "Transcription deleted"}

# 🔹 Borrar todas las transcripciones de un usuario
@router.delete("/delete-all-transcriptions")
async def delete_all_transcriptions(user_id: str = Depends(get_current_user)):
    """Deletes all transcriptions of the authenticated user."""
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Borrar las transcripciones del usuario
    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"transcriptions": []}}  # Reemplaza todas las transcripciones con una lista vacía
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No changes made")

    return {"message": "All transcriptions deleted"}
