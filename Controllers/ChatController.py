"""
Chat Controller - AI Chatbot
"""
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from Data.database import get_db
from Services.ChatService import ChatService

router = APIRouter(prefix="/Chat")


class ChatMessageRequest(BaseModel):
    """JSON request body cho chat API"""
    session_uuid: Optional[str] = None
    message: str


@router.get("/", response_class=HTMLResponse)
async def chat_page(request: Request, session_id: str = None, db: Session = Depends(get_db)):
    """Trang chatbot toàn màn hình"""
    chat_service = ChatService(db)
    session = chat_service.get_or_create_session(session_id)

    return templates.TemplateResponse(
        "Chat/index.html",
        {
            "request": request,
            "page_title": "Chat với AI",
            "session_uuid": session.session_uuid,
        }
    )


@router.post("/Send")
async def send_message(
    session_uuid: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    """Gửi tin nhắn (Form data - trang chat chính)"""
    chat_service = ChatService(db)

    try:
        response = chat_service.process_user_message(session_uuid, message)
        return JSONResponse({
            "success": True,
            "response": response,
            "session_uuid": session_uuid
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


@router.post("/Widget/Send")
async def widget_send_message(
    request: Request,
    body: ChatMessageRequest,
    db: Session = Depends(get_db),
):
    """Gửi tin nhắn từ chatbox popup (JSON API)"""
    chat_service = ChatService(db)

    # Lấy account_id từ user đang login (nếu có)
    account_id = None
    current_user = getattr(request.state, "current_user", None)
    if current_user:
        account_id = current_user.account_id

    # Tạo session nếu chưa có
    session_uuid = body.session_uuid
    if not session_uuid:
        session = chat_service.create_session(account_id)
        session_uuid = session.session_uuid

    try:
        response = chat_service.process_user_message(
            session_uuid, body.message, account_id
        )
        return JSONResponse({
            "success": True,
            "response": response,
            "session_uuid": session_uuid,
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e),
        }, status_code=500)


@router.post("/Widget/Init")
async def widget_init(request: Request, db: Session = Depends(get_db)):
    """Khởi tạo session cho chatbox popup"""
    chat_service = ChatService(db)

    account_id = None
    current_user = getattr(request.state, "current_user", None)
    if current_user:
        account_id = current_user.account_id

    session = chat_service.create_session(account_id)
    return JSONResponse({
        "success": True,
        "session_uuid": session.session_uuid,
    })


@router.get("/History/{session_uuid}")
async def get_history(session_uuid: str, db: Session = Depends(get_db)):
    """Lấy lịch sử chat"""
    chat_service = ChatService(db)
    session = chat_service.get_session(session_uuid)

    if not session:
        raise HTTPException(status_code=404, detail="Session không tìm thấy")

    messages = chat_service.get_session_messages(session.session_id)

    return JSONResponse({
        "session_uuid": session_uuid,
        "messages": [
            {
                "sender": msg.sender_type,
                "content": msg.message_content,
                "created_at": msg.created_at.isoformat() if msg.created_at else None
            }
            for msg in messages
        ]
    })


# Templates
templates = None

def set_templates(t):
    global templates
    templates = t
