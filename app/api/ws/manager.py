from fastapi import WebSocket, WebSocketDisconnect
from app.models.chat import ChatRoom, ChatMessage, ChartData, Content
import uuid
from app.api.ws.helper import WsHelper

class WsManager:
    def __init__(self):
        self.rooms: dict[str, ChatRoom] = {}

     #  handle connect ws
    async def connectUser(self, ws: WebSocket) -> str:
        try:
            room_id = ws.query_params.get('room_id')
            if not room_id or room_id not in self.rooms:
                room_id = str(uuid.uuid4())
                self.rooms[room_id] = ChatRoom(room_id,ws)
            else:
                self.rooms[room_id].user = ws
            return room_id
        except Exception as e:
            print(e)