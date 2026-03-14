from fastapi import WebSocket, APIRouter
from app.agents.intent_router import route_intent

router = APIRouter()

@router.websocket('/chat')
async def chat_ws(ws: WebSocket):
    await ws.accept()
    rawQuery = await ws.receive_text()
    ai_res = await route_intent(rawQuery)
    await ws.send_text(ai_res)