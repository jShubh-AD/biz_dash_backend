from fastapi import HTTPException, Path
from app.api.ws.manager import manager

def validate_room(room_id: str = Path(...)):
    room = manager.rooms.get(room_id)
    if not room: raise HTTPException(status_code=400, detail="No room or incorrect room_id")
    return room