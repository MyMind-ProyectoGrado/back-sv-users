from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Literal
from datetime import datetime, date
from .transcription_schema import Transcription


class UpdateNotificationsRequest(BaseModel):
    notifications: bool

class UpdateProfilePicRequest(BaseModel):
    profilePic: str
    
class PrivacyPreferences(BaseModel):
    allow_anonimized_usage: bool


class DataTreatment(BaseModel):
    accept_policies: bool
    acceptance_date: datetime
    acceptance_ip: str
    privacy_preferences: PrivacyPreferences

    @validator("acceptance_ip")
    def validate_ip(cls, v):
        """Validate that the IP address follows a correct format."""
        import re
        ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$" 
        if not re.match(ip_pattern, v):
            raise ValueError("Invalid IP address format")
        return v


class UserSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)  
    email: EmailStr  
    profilePic: Optional[str] = None
    birthdate: str
    city: str 
    personality: Optional[Literal["Introvertido", "Extrovertido"]] = None 
    university: str 
    degree: str 
    gender: Optional[Literal["Masculino", "Femenino", "Omitido"]] = None  
    notifications: bool
    data_treatment: DataTreatment
    transcriptions: List[Transcription] = []  

    @validator("name")
    def validate_name(cls, v):
        """Validates that the name is not too short or too long."""
        if len(v.strip()) < 1:
            raise ValueError("Name cannot be empty")
        if len(v) > 100:
            raise ValueError("Name cannot be longer than 100 characters")
        return v

    @validator("notifications")
    def validate_notifications(cls, v):
        """Ensure that notifications is a boolean value."""
        if not isinstance(v, bool):
            raise ValueError("Notifications must be a boolean value")
        return v
    @validator("birthdate")
    def validate_date_format(cls, v):
        """Validate that the date is in the correct format (e.g., ISO format)."""
        try:
            datetime.fromisoformat(v)  
        except ValueError:
            raise ValueError("Invalid date format, expected ISO format")
        return v