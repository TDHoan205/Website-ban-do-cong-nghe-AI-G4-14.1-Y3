"""
AI Chat Service - RAG Pipeline cho Chatbot
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from Models.Chat import ChatSession, ChatMessage, FAQ
from Services.AI.RAGEngine import RAGEngine
import uuid
import re
import unicodedata
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
        Nếu user muốn nói chuyện nhân viên → chuyển sang live chat
        """
        # Tạo hoặc lấy session
        session = self.get_or_create_session(session_uuid, account_id)

        # Kiểm tra nếu user muốn nói chuyện với nhân viên
        if self._is_live_chat_request(user_message):
            return self._handle_live_chat_request(session, account_id)

        # Lưu tin nhắn user
        self.add_message(session.session_id, "user", user_message)

        faq_response = self._find_direct_faq_answer(user_message)
        if faq_response:
            self.add_message(session.session_id, "bot", faq_response, intent="faq")
            return faq_response

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

    def _normalize_text(self, text: str) -> str:
        text = (text or "").lower().strip()
        text = unicodedata.normalize("NFD", text)
        text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
        text = text.replace("đ", "d")
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def _tokens(self, text: str) -> set:
        stop_words = {
            "la", "cua", "va", "hay", "hoac", "cho", "voi", "nay", "do",
            "thi", "duoc", "co", "khong", "ban", "toi", "minh", "cai",
            "mot", "nhung", "cac", "nao", "gi", "sao", "the", "bao",
            "o", "tu", "den", "ve", "trong", "ngoai", "tren", "duoi",
            "a", "an", "the", "is", "are", "what", "how",
        }
        return {
            token for token in self._normalize_text(text).split()
            if len(token) >= 2 and token not in stop_words
        }

    def _find_direct_faq_answer(self, user_message: str) -> Optional[str]:
        """
        Ưu tiên trả lời FAQ nội bộ trước khi gọi LLM.
        Threshold cao (0.80) để tránh false positive — chỉ match khi câu hỏi
        thực sự rất gần với FAQ, không dùng cho câu hỏi mơ hồ.
        """
        user_tokens = self._tokens(user_message)
        # Bỏ qua nếu câu quá ngắn (< 3 tokens) — dễ match nhầm
        if len(user_tokens) < 3:
            return None

        faqs = self.db.query(FAQ).filter(FAQ.is_active == True).all()
        best_faq = None
        best_score = 0.0

        for faq in faqs:
            question_tokens = self._tokens(faq.question)
            if not question_tokens:
                continue

            answer_tokens = self._tokens(faq.answer)
            faq_tokens = question_tokens | answer_tokens

            overlap = len(user_tokens & faq_tokens)
            question_overlap = len(user_tokens & question_tokens)

            # Phải match ít nhất 2 token trong câu hỏi FAQ
            if question_overlap < 2:
                continue

            score = (
                (overlap / max(len(user_tokens), 1))
                + (question_overlap / max(len(question_tokens), 1))
            )

            # Bonus nếu câu hỏi gần giống hệt
            normalized_question = self._normalize_text(faq.question)
            normalized_user = self._normalize_text(user_message)
            if normalized_question and (
                normalized_question in normalized_user
                or normalized_user in normalized_question
            ):
                score += 1.0

            if score > best_score:
                best_score = score
                best_faq = faq

        # Threshold 0.80 (tăng từ 0.62) — chỉ trả lời thẳng khi khớp rất cao
        if best_faq and best_score >= 0.80:
            return best_faq.answer
        return None

    def _is_live_chat_request(self, message: str) -> bool:
        """Kiểm tra user có muốn nói chuyện với nhân viên không"""
        msg = message.lower().strip()
        keywords = [
            "nói chuyện với nhân viên",
            "chat với nhân viên",
            "gặp nhân viên",
            "kết nối nhân viên",
            "liên hệ nhân viên",
            "muốn gặp người thật",
            "chat với người thật",
            "nhắn với nhân viên",
            "tư vấn viên",
            "hỗ trợ trực tiếp",
            "talk to staff",
            "human support",
            "live chat",
        ]
        return any(kw in msg for kw in keywords)

    def _handle_live_chat_request(self, session, account_id: int = None) -> str:
        """Tạo yêu cầu live chat và trả về thông báo"""
        from Services.LiveChatService import LiveChatService

        live_chat_service = LiveChatService(self.db)

        # Lấy tên khách hàng nếu đăng nhập
        customer_name = "Khách vãng lai"
        if account_id:
            from Models.Account import Account
            account = self.db.query(Account).filter(Account.account_id == account_id).first()
            if account and account.full_name:
                customer_name = account.full_name

        conversation = live_chat_service.request_live_chat(
            session_id=session.session_id,
            customer_account_id=account_id,
            customer_name=customer_name,
            subject="Hỗ trợ khách hàng",
        )

        # Lưu tin nhắn vào chat session
        self.add_message(session.session_id, "user", "Yêu cầu nói chuyện với nhân viên")
        self.add_message(
            session.session_id, "bot",
            "Đang kết nối bạn với nhân viên hỗ trợ...",
            intent="live_chat_request",
        )

        # Trả về response đặc biệt (chứa conversation_id để frontend chuyển mode)
        return f"__LIVECHAT__{conversation.conversation_id}__Đang kết nối bạn với nhân viên hỗ trợ. Vui lòng đợi trong giây lát... 💬"

