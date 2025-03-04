from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class AgentResponse(BaseModel):
    response: Message

class ErrorResponse(BaseModel):
    error: str