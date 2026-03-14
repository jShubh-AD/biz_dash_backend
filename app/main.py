from fastapi import FastAPI
from app.api.ws.chat import router as chat_router


app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(chat_router, prefix='/ws')