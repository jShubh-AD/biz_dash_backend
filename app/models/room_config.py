from pydantic import BaseModel

ALLOWED_MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-1.5-flash"
]

class RoomOperations(BaseModel):
    label: str
    action: str 

class AppConfig(BaseModel):
    ai_models: str
    api_key: str
    app_operations: list[RoomOperations]   

class RoomConfig(BaseModel):
    ai_model: str
    api_key: str | None = None