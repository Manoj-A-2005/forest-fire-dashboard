from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import asyncio
import threading
import os

from services.video_stream import generate_frames, inference_loop
from services.realtime_state import current_state

# Load Telegram configuration from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# If chat id is numeric, convert to int to match Telegram API expectations
if TELEGRAM_CHAT_ID and TELEGRAM_CHAT_ID.isdigit():
    TELEGRAM_CHAT_ID = int(TELEGRAM_CHAT_ID)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 START INFERENCE THREAD SAFELY
@app.on_event("startup")
def start_background_tasks():
    threading.Thread(target=inference_loop, daemon=True).start()
    print("🔥 Inference thread started")

@app.get("/video-feed")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

class TelegramAlert(BaseModel):
    message: str

@app.post("/send-telegram-alert")
def send_telegram_alert(alert: TelegramAlert):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {"status": "failed", "error": "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set"}

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": alert.message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        return {"status": "failed", "error": response.text}

    return {"status": "sent"}


@app.websocket("/ws/realtime")
async def realtime_ws(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket connected")

    try:
        while True:
            await websocket.send_json({
                "confidence": current_state["confidence"],
                "status": current_state["status"],
                "lat": current_state["lat"],
                "lon": current_state["lon"],
                "updated_at": current_state["updated_at"]
            })
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("❌ WebSocket disconnected")


