from pydantic import BaseModel, Field, validator
from typing import Dict, Optional
from datetime import datetime

class IdRequest(BaseModel):
    transcription_id: str

class EmotionRequest(BaseModel):
    emotion: str

class SentimentRequest(BaseModel):
    sentiment: str

class TopicRequest(BaseModel):
    topic: str

class DateRequest(BaseModel):
    date: str

class HourRequest(BaseModel):
    start_hour: int
    end_hour: Optional[int] = None

class Transcription(BaseModel):
    date: str
    time: str
    text: str = Field(..., min_length=1)  
    emotion: str = Field(..., min_length=1)  
    emotionProbabilities: Dict[str, float]  
    sentiment: str = Field(..., min_length=1)  
    sentimentProbabilities: Dict[str, float]  
    topic: Optional[str] = None 

    @validator("date")
    def validate_date_format(cls, v):
        """Validate that the date is in the correct format (e.g., ISO format)."""
        try:
            datetime.fromisoformat(v)  
        except ValueError:
            raise ValueError("Invalid date format, expected ISO format")
        return v
