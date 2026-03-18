from fastapi import HTTPException, APIRouter, Depends
from app.models.room_config import RoomConfig, ALLOWED_MODELS
from app.api.http.dependencies.room_id import validate_room
from app.api.ws.manager import  manager
from google import genai

router = APIRouter()

@router.post('/rooms/{room_id}')
async def set_config(
    body: RoomConfig,
    room= Depends(validate_room),
    ):
    room.api_key = body.api_key
    room.ai_model = body.ai_model
    room.client = genai.Client(api_key=room.api_key)
    return {
            "success": True,
            "status": 200,
            "message": "Config set successfully"
        }

@router.get("/rooms/{room_id}")
async def get_room_config(room = Depends(validate_room),):
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
async def delete_room(room= Depends(validate_room)):
    manager.rooms.pop(room.id, None)
    return {
      "success": True,
      "status": 200,
      "message": "Config fetched successfully",
    }


@router.get("/models}")
async def get_room_models():
    return {
      "success": True,
      "status": 200,
      "message": "Config fetched successfully",
      "data": ALLOWED_MODELS
    }