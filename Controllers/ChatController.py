"""
Chat Controller - AI Chatbot + Live Chat
"""
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from Data.database import get_db
from Services.ChatService import ChatService
from Services.LiveChatService import LiveChatService

router = APIRouter(prefix="/Chat")


class ChatMessageRequest(BaseModel):
    """JSON request body cho chat API"""
    session_uuid: Optional[str] = None
    message: str


class LiveChatMessageRequest(BaseModel):
    """JSON request body cho live chat"""
    conversation_id: int
    message: str


@router.get("/", response_class=HTMLResponse)
async def chat_page(request: Request, session_id: str = None, db: Session = Depends(get_db)):
    """Trang chatbot toàn màn hình"""
    if templates is None:
        from fastapi.responses import Response
        return Response("Templates chưa được khởi tạo", status_code=503)

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
        result = chat_service.process_user_message_full(
            session_uuid, body.message, account_id
        )
        response = result["response"]
        intent = result.get("intent", "general")
        buy_products = result.get("buy_products", [])

        # Kiểm tra nếu response là live chat request
        if response.startswith("__LIVECHAT__"):
            parts = response.split("__", 4)
            conversation_id = int(parts[2])
            display_message = parts[3] if len(parts) > 3 else "Đang kết nối nhân viên..."
            return JSONResponse({
                "success": True,
                "response": display_message,
                "session_uuid": session_uuid,
                "live_chat": True,
                "conversation_id": conversation_id,
            })

        # Nếu có intent mua hàng + tìm thấy sản phẩm → trả action buy
        if intent == "buy_intent" and buy_products:
            in_stock = [p for p in buy_products if p.get("stock", 0) > 0]
            products_payload = [
                {
                    "product_id": p["id"],
                    "product_name": p["name"],
                    "price": p.get("price", 0),
                }
                for p in (in_stock or buy_products)[:3]
            ]
            return JSONResponse({
                "success": True,
                "response": response,
                "session_uuid": session_uuid,
                "action": "add_to_cart",
                "products": products_payload,
            })

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


# =====================================================================
# LIVE CHAT ENDPOINTS (Customer side)
# =====================================================================

@router.post("/LiveChat/Request")
async def livechat_request(request: Request, db: Session = Depends(get_db)):
    """Khách yêu cầu nói chuyện với nhân viên"""
    live_chat_service = LiveChatService(db)
    chat_service = ChatService(db)

    account_id = None
    customer_name = "Khách vãng lai"
    current_user = getattr(request.state, "current_user", None)
    if current_user:
        account_id = current_user.account_id
        customer_name = current_user.full_name or current_user.username

    # Lấy session_id từ body nếu có
    try:
        body = await request.json()
        session_uuid = body.get("session_uuid")
    except Exception:
        session_uuid = None

    session_id = None
    if session_uuid:
        session = chat_service.get_session(session_uuid)
        if session:
            session_id = session.session_id

    conversation = live_chat_service.request_live_chat(
        session_id=session_id,
        customer_account_id=account_id,
        customer_name=customer_name,
        subject="Hỗ trợ khách hàng",
    )

    return JSONResponse({
        "success": True,
        "conversation_id": conversation.conversation_id,
        "status": conversation.status,
    })


@router.post("/LiveChat/Send")
async def livechat_send(
    request: Request,
    body: LiveChatMessageRequest,
    db: Session = Depends(get_db),
):
    """Khách gửi tin nhắn trong live chat"""
    live_chat_service = LiveChatService(db)

    account_id = None
    current_user = getattr(request.state, "current_user", None)
    if current_user:
        account_id = current_user.account_id

    message = live_chat_service.send_customer_message(
        conversation_id=body.conversation_id,
        content=body.message,
        customer_account_id=account_id,
    )

    if not message:
        return JSONResponse({
            "success": False,
            "error": "Cuộc hội thoại đã kết thúc hoặc không tồn tại",
        }, status_code=400)

    return JSONResponse({
        "success": True,
        "message_id": message.message_id,
    })


@router.get("/LiveChat/Messages/{conversation_id}")
async def livechat_messages(
    conversation_id: int,
    after_id: int = 0,
    db: Session = Depends(get_db),
):
    """Lấy tin nhắn live chat (polling)"""
    live_chat_service = LiveChatService(db)

    # Đánh dấu đã đọc tin nhắn từ staff
    live_chat_service.mark_messages_read(conversation_id, "customer")

    messages = live_chat_service.get_messages(conversation_id, after_id)

    # Lấy status conversation
    conv = live_chat_service._get_conversation(conversation_id)
    status = conv.status if conv else "closed"

    return JSONResponse({
        "success": True,
        "status": status,
        "messages": [
            {
                "message_id": msg.message_id,
                "sender_type": msg.sender_type,
                "content": msg.content,
                "created_at": msg.created_at.strftime("%H:%M") if msg.created_at else "",
            }
            for msg in messages
        ],
    })


@router.get("/LiveChat/Status")
async def livechat_status(
    request: Request,
    session_uuid: str = None,
    db: Session = Depends(get_db),
):
    """Kiểm tra khách có cuộc live chat đang active không"""
    live_chat_service = LiveChatService(db)
    chat_service = ChatService(db)

    account_id = None
    current_user = getattr(request.state, "current_user", None)
    if current_user:
        account_id = current_user.account_id

    session_id = None
    if session_uuid:
        session = chat_service.get_session(session_uuid)
        if session:
            session_id = session.session_id

    conversation = live_chat_service.get_active_conversation_by_customer(
        customer_account_id=account_id,
        session_id=session_id,
    )

    if conversation:
        return JSONResponse({
            "success": True,
            "active": True,
            "conversation_id": conversation.conversation_id,
            "status": conversation.status,
        })

    return JSONResponse({
        "success": True,
        "active": False,
    })


# Templates
templates = None

def set_templates(t):
    global templates
    templates = t

