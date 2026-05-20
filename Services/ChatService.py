"""
AI Chat Service - RAG Pipeline cho Chatbot
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from Models.Chat import ChatSession, ChatMessage
from Services.AI.RAGEngine import RAGEngine
import uuid
from datetime import datetime


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.rag_engine = RAGEngine(db)

    def create_session(self, account_id: Optional[int] = None) -> ChatSession:
        """Tạo phiên chat mới"""
        session = ChatSession(
            session_uuid=str(uuid.uuid4()),
            account_id=account_id,
            is_active=True
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_uuid: str) -> Optional[ChatSession]:
        """Lấy phiên chat theo UUID"""
        return self.db.query(ChatSession).filter(
            ChatSession.session_uuid == session_uuid
        ).first()

    def get_or_create_session(self, session_uuid: str = None, account_id: int = None) -> ChatSession:
        """Lấy hoặc tạo phiên chat"""
        if session_uuid:
            session = self.get_session(session_uuid)
            if session:
                return session
        return self.create_session(account_id)

    def add_message(
        self,
        session_id: int,
        sender_type: str,
        content: str,
        intent: str = None,
        confidence_score: str = None
    ) -> ChatMessage:
        """Thêm tin nhắn vào phiên chat"""
        message = ChatMessage(
            session_id=session_id,
            sender_type=sender_type,
            message_content=content,
            intent=intent,
            confidence_score=confidence_score
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_session_messages(self, session_id: int) -> List[ChatMessage]:
        """Lấy lịch sử tin nhắn của phiên chat"""
        return self.db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at).all()

    def end_session(self, session_uuid: str) -> bool:
        """Kết thúc phiên chat"""
        session = self.get_session(session_uuid)
        if session:
            session.is_active = False
            session.ended_at = datetime.now()
            self.db.commit()
            return True
        return False

    def process_user_message(self, session_uuid: str, user_message: str, account_id: int = None) -> str:
        """
        Xử lý tin nhắn từ user qua RAG Pipeline thực tế
        """
        # Tạo hoặc lấy session
        session = self.get_or_create_session(session_uuid, account_id)

        # Lưu tin nhắn user
        self.add_message(session.session_id, "user", user_message)

        # Lấy conversation history — giới hạn 6 tin (3 lượt) để tiết kiệm tokens
        history_msgs = self.get_session_messages(session.session_id)
        conversation_history = [
            {"sender": msg.sender_type, "content": msg.message_content}
            for msg in history_msgs[-6:]  # 6 tin nhắn gần nhất
        ]

        # Gọi RAG Engine
        try:
            result = self.rag_engine.get_response(
                user_message=user_message,
                conversation_history=conversation_history,
                account_id=account_id,
            )
            response = result["response"]
            intent = result.get("intent", "general")
        except Exception as e:
            print(f"[ChatService] RAG Error: {e}")
            response = "Xin lỗi, hệ thống đang gặp sự cố. Vui lòng thử lại sau! 🙏"
            intent = "error"

        # Lưu tin nhắn bot
        self.add_message(session.session_id, "bot", response, intent=intent)

        return response
