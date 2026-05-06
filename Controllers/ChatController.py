"""
Chat Controller - AI Chatbot
"""
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Services.ChatService import ChatService

router = APIRouter(prefix="/Chat")


@router.get("/", response_class=HTMLResponse)
async def chat_page(request: Request, session_id: str = None, db: Session = Depends(get_db)):
    """Trang chatbot"""
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
    """Gửi tin nhắn và nhận phản hồi"""
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
