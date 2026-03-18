from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import WebSocket
from typing import Any
from app.constants.app_enum import MessageType, RoleEnums
from app.models.room_config import ALLOWED_MODELS
from google import genai

# chats model
class ChartData(BaseModel):
    labels: list[str | int | float]
    values: list[int | float]
    x_axis: str
    y_axis: str

#  chat messages model
class ChatMessage (BaseModel):
    id: str
    type: MessageType = MessageType.query
    role: RoleEnums
    data: ChartData | str

#  Schema model
class Schema (BaseModel):
    columns: list[str]=[]
    sample: dict[str,Any] = {}

#  chat rooms stores all conversation locally on server
class ChatRoom:
    def __init__(self, room_id, user: WebSocket):
        self.messages: list[ChatMessage] = []
        self.room_id = room_id
        self.ai_model = ALLOWED_MODELS[0]
        self.api_key: str | None = None
        self.client: genai.Client | None = None
        self.user= user
        self.table_name: str
        self.schema: Schema = Schema()
        self.context: list[ChatMessage] = []
        self.created_at = datetime.utcnow()

