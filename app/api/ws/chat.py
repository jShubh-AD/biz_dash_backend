from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from app.api.ws.manager import manager

router = APIRouter()

@router.websocket('/chat')
async def chat_ws(ws: WebSocket):
    await ws.accept()
    room_id = await manager.connectUser(ws)
    ws.state.room_id = room_id
    await ws.send_json({"room_id": f"{room_id}"}) 
    try: 
        while True:
            data = await ws.receive_json()
            await manager.handleReceiver(ws,data)
    except WebSocketDisconnect: 
        print("ws disconnect")
