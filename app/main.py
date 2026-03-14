from fastapi import FastAPI
from fastapi import WebSocket

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

