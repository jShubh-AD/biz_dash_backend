from fastapi import WebSocket, WebSocketDisconnect
from app.constants.app_enum import RoleEnums, MessageType, ProgressStatus
from app.models.chat import ChatRoom, ChatMessage, ChartData
import uuid
from app.api.ws.helper import WsHelper
from app.agents.chart_agent import ChartAgent
from app.agents.sql_agent import SQLAgent
from app.agents.explanation_agent import ExplanationAgent

class WsManager:
    def __init__(self):
        self.rooms: dict[str, ChatRoom] = {}

    async def check_have_db(self,room: ChatRoom):
         if room.have_db is False:
            return ChatMessage(
                id=str(uuid.uuid4()),
                type= MessageType.error,
                role=RoleEnums.assistent,
                data='No Data set is provided'
                )

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
            await ws.send_json({"status":ProgressStatus.error, "data": str(e)})  
            ws.close()
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

            response = await self._route_message(room, msg)
            room.messages.append(response)

            await ws.send_json({"status":ProgressStatus.successs, "data": response.model_dump()})     

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
            type = data.get("type", MessageType.query),
            data=data["data"]
        )
    
    async def _route_message(self, room : ChatRoom, msg : ChatMessage):
        match msg.type:
            case MessageType.query:
                guard = await self.check_have_db(room)
                if guard:
                    return guard
                agent = ExplanationAgent()
                response = await agent.handle(query=msg.data, room= room)
                return response
            case MessageType.chart:
                guard = await self.check_have_db(room)
                if guard:
                    return guard
                agent = ChartAgent()
                response = await agent.handle(query=msg.data, room= room)
                return response
            case MessageType.explanation:
                guard = await self.check_have_db(room)
                if guard:
                    return guard
                await self.check_have_db(room)
                agent = ExplanationAgent()
                response = await agent.handle(query=msg.data, room= room)
                return response
            


manager = WsManager()

