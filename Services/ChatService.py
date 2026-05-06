"""
AI Chat Service - RAG Pipeline cho Chatbot
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from Models.Chat import ChatSession, ChatMessage
import uuid
from datetime import datetime


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_id: Optional[int] = None) -> ChatSession:
        """Tạo phiên chat mới"""
        session = ChatSession(
            session_uuid=str(uuid.uuid4()),
            user_id=user_id,
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

    def get_or_create_session(self, session_uuid: str = None, user_id: int = None) -> ChatSession:
        """Lấy hoặc tạo phiên chat"""
        if session_uuid:
            session = self.get_session(session_uuid)
            if session:
                return session
        return self.create_session(user_id)

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

    def process_user_message(self, session_uuid: str, user_message: str, user_id: int = None) -> str:
        """
        Xử lý tin nhắn từ user và trả lời
        Đây là placeholder - sẽ tích hợp RAG pipeline thực tế
        """
        # Tạo hoặc lấy session
        session = self.get_or_create_session(session_uuid, user_id)

        # Lưu tin nhắn user
        self.add_message(session.session_id, "user", user_message)

        # TODO: Tích hợp RAG pipeline thực tế
        # response = self.rag_pipeline.get_response(user_message)

        # Placeholder response
        response = self._generate_response(user_message)

        # Lưu tin nhắn bot
        self.add_message(session.session_id, "bot", response)

        return response

    def _generate_response(self, user_message: str) -> str:
        """Placeholder - Tạo phản hồi mẫu"""
        user_message_lower = user_message.lower()

        if any(word in user_message_lower for word in ["iphone", "samsung", "laptop", "macbook"]):
            return "Cảm ơn bạn đã quan tâm! Tôi có thể giúp bạn tìm sản phẩm phù hợp. Bạn muốn tìm sản phẩm nào cụ thể không?"
        elif any(word in user_message_lower for word in ["giá", "price", "bao nhiêu", "cost"]):
            return "Bạn có thể xem giá chi tiết từng sản phẩm tại trang sản phẩm của chúng tôi. Giá được cập nhật liên tục!"
        elif any(word in user_message_lower for word in ["mua", "đặt", "order", "đặt hàng"]):
            return "Để đặt hàng, bạn có thể thêm sản phẩm vào giỏ hàng và tiến hành checkout. Tôi có thể hướng dẫn bạn từng bước!"
        elif any(word in user_message_lower for word in ["xin chào", "hello", "hi", "chào"]):
            return "Xin chào! Tôi là trợ lý AI của Tech Store. Tôi có thể giúp bạn tìm sản phẩm công nghệ, so sánh giá, và tư vấn mua hàng. Bạn cần hỗ trợ gì hôm nay?"
        else:
            return "Cảm ơn tin nhắn của bạn! Tôi có thể giúp bạn về sản phẩm công nghệ, giá cả, và đơn hàng. Bạn cứ hỏi nhé!"
