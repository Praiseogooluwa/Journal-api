from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime, date as dt_date

class MoodEnum(str, Enum):
    GOOD = "good"
    NEUTRAL = "neutral"
    BAD = "bad"

class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class EntryCreate(BaseModel):
    title: str
    content: str
    mood: MoodEnum
    date: dt_date
    tags: Optional[List[str]] = []

class EntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[MoodEnum] = None
    date: Optional[dt_date] = None

class EntryResponse(BaseModel):
    id: int
    title: str
    content: str
    mood: str
    date: dt_date
    created_at: datetime
    user_id: int
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True