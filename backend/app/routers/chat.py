from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Dict, Optional
from datetime import datetime
import json
import uuid
from app.core.database import get_db
from app.core.security import decode_token
from app.services.chatbot_service import ChatBotService
from app.schemas.chat import ChatMessage, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

active_connections: Dict[str, list] = {}


@router.post("/", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    db: Session = Depends(get_db)
):
    chat_service = ChatBotService(db)
    session_id = message.session_id or str(uuid.uuid4())

    result = chat_service.process_message(message.message, message.context)

    return ChatResponse(
        response=result["response"],
        session_id=session_id,
        intent=result["intent"],
        action=result.get("action"),
        suggested_products=result.get("suggested_products"),
        timestamp=datetime.utcnow(),
    )


class ConnectionManager:
    @staticmethod
    async def connect(websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in active_connections:
            active_connections[session_id] = []
        active_connections[session_id].append(websocket)

    @staticmethod
    def disconnect(websocket: WebSocket, session_id: str):
        if session_id in active_connections:
            if websocket in active_connections[session_id]:
                active_connections[session_id].remove(websocket)
            if not active_connections[session_id]:
                del active_connections[session_id]

    @staticmethod
    async def send_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)


@router.websocket("/ws/{session_id}")
async def websocket_chat(
    websocket: WebSocket,
    session_id: str,
    db: Session = Depends(get_db)
):
    await ConnectionManager.connect(websocket, session_id)
    chat_service = ChatBotService(db)

    try:
        await websocket.send_json({
            "type": "system",
            "message": "Đã kết nối với chatbot. Bắt đầu trò chuyện!",
            "timestamp": datetime.utcnow().isoformat(),
        })

        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                user_message = payload.get("message", "")
                token = payload.get("token")

                if token:
                    user_data = decode_token(token)
                    context = {"user": user_data}
                else:
                    context = None

                result = chat_service.process_message(user_message, context)

                await websocket.send_json({
                    "type": "assistant",
                    "message": result["response"],
                    "intent": result["intent"],
                    "suggested_products": result.get("suggested_products"),
                    "action": result.get("action"),
                    "timestamp": datetime.utcnow().isoformat(),
                })

            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid message format",
                })

    except WebSocketDisconnect:
        ConnectionManager.disconnect(websocket, session_id)
