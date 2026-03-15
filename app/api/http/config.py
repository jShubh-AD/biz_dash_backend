from fastapi import HTTPException, Response, Request, APIRouter, FastAPI
from app.models.chat import ChatRoom
from app.models.room_config import RoomConfig
from app.api.ws.manager import  manager
from google import genai

router = APIRouter()

@router.post('/rooms/{room_id}')
async def setConfig(room_id: str, body: RoomConfig):
    room = manager.rooms.get(room_id)
    if not room: return HTTPException(status_code=400, detail="No room or incorrect room_id")
    room.api_key = body.api_key
    room.ai_model = body.ai_model
    room.client = genai.Client(api_key=room.api_key)
    return {
            "success": True,
            "status": 200,
            "message": "Config set successfully"
        }

@router.get("/rooms/{room_id}")
async def getRoomConfig(room_id: str):
    room = manager.rooms.get(room_id)
    if not room: return HTTPException(status_code=400, detail="No room or incorrect room_id")
    return {
      "success": True,
      "status": 200,
      "message": "Config fetched successfully",
      "data": RoomConfig(
          ai_model=room.ai_model,
          api_key=room.api_key
      ).model_dump()
    }

@router.delete("/rooms/{room_id}")
async def deleteRoom(room_id: str):
    room = manager.rooms.get(room_id)
    if not room: return HTTPException(status_code=400, detail="No room or incorrect room_id")
    manager.rooms.pop(room_id, None)
    return {
      "success": True,
      "status": 200,
      "message": "Config fetched successfully",
    }