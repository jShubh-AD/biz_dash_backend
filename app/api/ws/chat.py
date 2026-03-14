from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from app.agents.intent_router import route_intent
from app.api.ws.manager import WsManager

router = APIRouter()
manager = WsManager()

@router.websocket('/chat')
async def chat_ws(ws: WebSocket):
    await ws.accept()
    room_id = await manager.connectUser(ws)
    ws.state.room_id = room_id
    await ws.send_json({"room_id": f"{room_id}"}) 
    try: 
        while True:
            rawQuery = await ws.receive_text()
            ai_res = await route_intent(rawQuery)
            await ws.send_text(ai_res)
    except WebSocketDisconnect: 
        print("ws disconnect")
