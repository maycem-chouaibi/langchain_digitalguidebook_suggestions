from pydantic import BaseModel, Field
from typing import Dict, List


class Message(BaseModel):
    role: str
    content: str

class Location(BaseModel):
    address: str
    long: float
    lat: float

class Activity(BaseModel):
    title: str
    category: str
    description: str
    location: Location
    duration: str
    best_time: str
    price_range: float = Field(..., ge=1, le=5)
    rating: float = Field(..., ge=1, le=5)
    accessibility: str
    link: str

class AgentResponse(BaseModel):
    activities: List[Activity]

class ErrorResponse(BaseModel):
    error: str