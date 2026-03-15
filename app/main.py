from fastapi import FastAPI
from app.api.ws.chat import router as chat_router
from app.api.http.config import router as config_router


app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(chat_router, prefix='/ws')
app.include_router(config_router, prefix='/config')