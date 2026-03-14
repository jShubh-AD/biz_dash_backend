from fastapi import WebSocket, WebSocketDisconnect
from app.constants.app_enum import RoleEnums, MessageType, ProgressStatus
from app.models.chat import ChatRoom, ChatMessage, ChartData, Content
import uuid
from app.api.ws.helper import WsHelper
from app.agents.chart_agent import ChartAgent
from app.agents.sql_agent import SQLAgent
from app.agents.explanation_agent import ExplanationAgent

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

    #  handle receive json
    async def handleReceiver(self, ws: WebSocket, data: dict):
        try:
            # send loding state
            await ws.send_json({"status": ProgressStatus.loading})

            room = self._get_room(ws)
            if not room: return

            msg = self._create_message(data)
            room.messages.append(msg)

            response = await self._route_message(room, msg, ws)
            room.messages.append(response)

            await ws.send_json({"status":ProgressStatus.successs, "data": str(response.data)})     

        except Exception as e:
           await ws.send_json({"status":ProgressStatus.error, "data": str(e)})    
           print(e)



    def _get_room(self, ws: WebSocket):
        room_id = WsHelper.get_room_id(ws)
        return self.rooms.get(room_id)
    
    def _create_message(self, data: dict):
        return ChatMessage(
            id=str(uuid.uuid4()),
            role=RoleEnums.client,
            type=data["type"],
            data=data["data"]
        )
    
    async def _route_message(self, room : ChatRoom, msg : ChatMessage, ws: WebSocket):
        match msg.type:
            case MessageType.query:
                agent = ExplanationAgent()
                response = await agent.handle(query=msg.data)
                return response
            case MessageType.chart:
                print("send to make cahrt")
            case MessageType.error:
                await ws.send_json({"status": ProgressStatus.error})
                print("some error occurred")