from fastapi import FastAPI
from app.api.ws.chat import router as chat_router
from app.api.http.config import router as config_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bi-zeta-five.vercel.app",
        "http://localhost:5173"
        "http://localhost:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(chat_router, prefix='/ws')
app.include_router(config_router, prefix='/config')