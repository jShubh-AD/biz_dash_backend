from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import WebSocket
from app.constants.app_enum import MessageType, RoleEnums

#  chat rooms stores all conversation locally on server
class ChatRoom:
    def __init__(self, room_id, user: WebSocket):
        self.messages: list[ChatMessage] = []
        self.room_id = room_id
        self.user= user
        self.context: list[ChatMessage] = []
        self.created_at = datetime.utcnow()


# chats model
class ChartData(BaseModel):
    labels: list[str]
    values: list[int]

#  Message data/content
class Content(BaseModel):
    data: ChartData | str

#  chat messages model
class ChatMessage (BaseModel):
    id: str
    type: MessageType = MessageType.query
    role: RoleEnums
    data: Content | str
    created_at: datetime = Field(default_factory=datetime.utcnow)

