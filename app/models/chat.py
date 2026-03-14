from datetime import datetime
from pydantic import BaseModel
from fastapi import WebSocket
from app.constants.message_enum import MessageType

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
    data: ChartData | str | None = None

#  chat messages model
class ChatMessage (BaseModel):
    id: str
    type: MessageType
    role: str # ai or client
    data: Content | None = None
    created_at: datetime

