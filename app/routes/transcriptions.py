from fastapi import APIRouter, HTTPException, Depends, Query
from app.core.database import users_collection
from app.core.auth import get_current_user
from app.schemas.transcription_schema import Transcription
from typing import Optional
from bson import ObjectId

router = APIRouter()

# 🔹 Obtener todas las transcripciones
@router.get("/")
async def get_all_transcriptions(user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.get("transcriptions", [])

# 🔹 Obtener transcripción específica por ID
@router.get("/{transcription_id}")
async def get_transcription_by_id(transcription_id: str, user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transcription = next((t for t in user.get("transcriptions", []) if t["_id"] == transcription_id), None)
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcription not found")

    return transcription

# 🔹 Obtener transcripciones por emoción
@router.get("/by-emotion/{emotion}")
async def get_transcriptions_by_emotion(emotion: str, user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [t for t in user.get("transcriptions", []) if t.get("emotion") == emotion]

# 🔹 Obtener transcripciones por sentimiento
@router.get("/by-sentiment/{sentiment}")
async def get_transcriptions_by_sentiment(sentiment: str, user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [t for t in user.get("transcriptions", []) if t.get("sentiment") == sentiment]

# 🔹 Obtener transcripciones por tema
@router.get("/by-topic/{topic}")
async def get_transcriptions_by_topic(topic: str, user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [t for t in user.get("transcriptions", []) if t.get("topic") == topic]

# 🔹 Obtener transcripciones por fecha
@router.get("/by-date/{date}")
async def get_transcriptions_by_date(date: str, user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [t for t in user.get("transcriptions", []) if t.get("date", "").startswith(date)]

# 🔹 Obtener transcripciones por hora o rango de horas
@router.get("/by-hour/")
async def get_transcriptions_by_hour(
    start_hour: int,
    end_hour: Optional[int] = None,
    user_id: str = Depends(get_current_user)
):
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transcriptions = user.get("transcriptions", [])
    if end_hour is None:
        return [t for t in transcriptions if int(t.get("time", "00:00").split(":")[0]) == start_hour]
    else:
        return [t for t in transcriptions if start_hour <= int(t.get("time", "00:00").split(":")[0]) <= end_hour]

# 🔹 Obtener transcripciones con múltiples filtros
@router.get("/filter")
async def get_transcriptions_with_filters(
    emotion: Optional[str] = None,
    sentiment: Optional[str] = None,
    topic: Optional[str] = None,
    date: Optional[str] = None,
    start_hour: Optional[int] = Query(None, ge=0, le=23),
    end_hour: Optional[int] = Query(None, ge=0, le=23),
    user_id: str = Depends(get_current_user),
):
    user = await users_collection.find_one({"_id": user_id}, {"transcriptions": 1, "_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transcriptions = user.get("transcriptions", [])

    if emotion:
        transcriptions = [t for t in transcriptions if t.get("emotion") == emotion]
    if sentiment:
        transcriptions = [t for t in transcriptions if t.get("sentiment") == sentiment]
    if topic:
        transcriptions = [t for t in transcriptions if t.get("topic") == topic]
    if date:
        transcriptions = [t for t in transcriptions if t.get("date", "").startswith(date)]
    if start_hour is not None and end_hour is not None:
        transcriptions = [
            t for t in transcriptions if start_hour <= int(t.get("time", "00:00").split(":")[0]) <= end_hour
        ]
    return transcriptions

# 🔹 Insertar una nueva transcripción
@router.post("/add-transcription")
async def add_transcription(
    transcription: Transcription,
    user_id: str = Depends(get_current_user)
):
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Asegurar que _id va al principio
    transcription_data = {"_id": str(ObjectId())}
    transcription_data.update(transcription.dict())

    result = await users_collection.update_one(
        {"_id": user_id},
        {"$push": {"transcriptions": transcription_data}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to add transcription")

    return {"message": "Transcription added successfully", "transcription_id": transcription_data["_id"]}

# 🔹 Eliminar transcripción específica
@router.delete("/delete-transcription/{transcription_id}")
async def delete_transcription_by_id(transcription_id: str, user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await users_collection.update_one(
        {"_id": user_id},
        {"$pull": {"transcriptions": {"_id": transcription_id}}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Transcription not found")

    return {"message": "Transcription deleted"}

# 🔹 Eliminar todas las transcripciones
@router.delete("/delete-all-transcriptions")
async def delete_all_transcriptions(user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"transcriptions": []}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No changes made")

    return {"message": "All transcriptions deleted"}
