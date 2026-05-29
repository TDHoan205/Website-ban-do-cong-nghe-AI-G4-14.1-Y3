"""
Live Chat Service - Xử lý logic chat khách hàng ↔ nhân viên
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Dict
from Models.Chat import LiveChatConversation, LiveChatMessage, ChatSession
from datetime import datetime


class LiveChatService:
    def __init__(self, db: Session):
        self.db = db

    # ─────────────── CUSTOMER SIDE ───────────────

    def request_live_chat(
        self,
        session_id: int = None,
        customer_account_id: int = None,
        customer_name: str = None,
        subject: str = None,
    ) -> LiveChatConversation:
        """Khách hàng yêu cầu nói chuyện với nhân viên"""
        # Kiểm tra xem khách đã có cuộc hội thoại đang chờ/active chưa
        existing = self.get_active_conversation_by_customer(
            customer_account_id, session_id
        )
        if existing:
            return existing

        conversation = LiveChatConversation(
            session_id=session_id,
            customer_account_id=customer_account_id,
            customer_name=customer_name or "Khách vãng lai",
            subject=subject or "Hỗ trợ khách hàng",
            status="waiting",
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        # Thêm tin nhắn hệ thống
        system_msg = LiveChatMessage(
            conversation_id=conversation.conversation_id,
            sender_type="system",
            content="Khách hàng yêu cầu hỗ trợ. Đang chờ nhân viên kết nối...",
            is_read=True,
        )
        self.db.add(system_msg)
        self.db.commit()

        return conversation

    def get_active_conversation_by_customer(
        self,
        customer_account_id: int = None,
        session_id: int = None,
    ) -> Optional[LiveChatConversation]:
        """Lấy cuộc hội thoại đang waiting/active của khách"""
        query = self.db.query(LiveChatConversation).filter(
            LiveChatConversation.status.in_(["waiting", "active"])
        )
        if customer_account_id:
            query = query.filter(
                LiveChatConversation.customer_account_id == customer_account_id
            )
        elif session_id:
            query = query.filter(
                LiveChatConversation.session_id == session_id
            )
        else:
            return None
        return query.order_by(LiveChatConversation.created_at.desc()).first()

    def send_customer_message(
        self,
        conversation_id: int,
        content: str,
        customer_account_id: int = None,
    ) -> Optional[LiveChatMessage]:
        """Khách gửi tin nhắn"""
        conversation = self._get_conversation(conversation_id)
        if not conversation or conversation.status == "closed":
            return None

        message = LiveChatMessage(
            conversation_id=conversation_id,
            sender_type="customer",
            sender_account_id=customer_account_id,
            content=content,
            is_read=False,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    # ─────────────── STAFF SIDE ───────────────

    def get_waiting_conversations(self) -> List[LiveChatConversation]:
        """Danh sách cuộc hội thoại đang chờ nhân viên"""
        return (
            self.db.query(LiveChatConversation)
            .filter(LiveChatConversation.status == "waiting")
            .order_by(LiveChatConversation.created_at.asc())
            .all()
        )

    def get_active_conversations(self, staff_account_id: int = None) -> List[LiveChatConversation]:
        """Danh sách cuộc hội thoại đang active"""
        query = self.db.query(LiveChatConversation).filter(
            LiveChatConversation.status == "active"
        )
        if staff_account_id:
            query = query.filter(
                LiveChatConversation.staff_account_id == staff_account_id
            )
        return query.order_by(LiveChatConversation.created_at.desc()).all()

    def get_all_conversations(self) -> List[LiveChatConversation]:
        """Tất cả cuộc hội thoại (admin view)"""
        return (
            self.db.query(LiveChatConversation)
            .order_by(LiveChatConversation.created_at.desc())
            .all()
        )

    def accept_conversation(
        self, conversation_id: int, staff_account_id: int
    ) -> Optional[LiveChatConversation]:
        """Nhân viên nhận hỗ trợ cuộc hội thoại"""
        conversation = self._get_conversation(conversation_id)
        if not conversation or conversation.status != "waiting":
            return None

        conversation.staff_account_id = staff_account_id
        conversation.status = "active"
        conversation.accepted_at = datetime.now()
        self.db.commit()

        # Thêm tin nhắn hệ thống
        system_msg = LiveChatMessage(
            conversation_id=conversation_id,
            sender_type="system",
            content="Nhân viên đã kết nối. Bạn có thể trao đổi ngay bây giờ!",
            is_read=False,
        )
        self.db.add(system_msg)
        self.db.commit()

        self.db.refresh(conversation)
        return conversation

    def send_staff_message(
        self,
        conversation_id: int,
        content: str,
        staff_account_id: int,
    ) -> Optional[LiveChatMessage]:
        """Nhân viên gửi tin nhắn"""
        conversation = self._get_conversation(conversation_id)
        if not conversation or conversation.status != "active":
            return None

        message = LiveChatMessage(
            conversation_id=conversation_id,
            sender_type="staff",
            sender_account_id=staff_account_id,
            content=content,
            is_read=False,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def close_conversation(
        self, conversation_id: int
    ) -> Optional[LiveChatConversation]:
        """Kết thúc cuộc hội thoại"""
        conversation = self._get_conversation(conversation_id)
        if not conversation or conversation.status == "closed":
            return None

        conversation.status = "closed"
        conversation.closed_at = datetime.now()
        self.db.commit()

        # Thêm tin nhắn hệ thống
        system_msg = LiveChatMessage(
            conversation_id=conversation_id,
            sender_type="system",
            content="Cuộc hội thoại đã kết thúc. Cảm ơn bạn đã liên hệ!",
            is_read=True,
        )
        self.db.add(system_msg)
        self.db.commit()

        self.db.refresh(conversation)
        return conversation

    # ─────────────── SHARED ───────────────

    def get_messages(
        self, conversation_id: int, after_id: int = 0
    ) -> List[LiveChatMessage]:
        """Lấy tin nhắn, hỗ trợ polling (chỉ lấy sau after_id)"""
        query = self.db.query(LiveChatMessage).filter(
            LiveChatMessage.conversation_id == conversation_id
        )
        if after_id > 0:
            query = query.filter(LiveChatMessage.message_id > after_id)
        return query.order_by(LiveChatMessage.created_at.asc()).all()

    def mark_messages_read(
        self, conversation_id: int, reader_type: str
    ) -> int:
        """Đánh dấu đã đọc (reader_type: customer hoặc staff)"""
        # Đánh dấu tin nhắn của đối phương là đã đọc
        opposite = "staff" if reader_type == "customer" else "customer"
        updated = (
            self.db.query(LiveChatMessage)
            .filter(
                LiveChatMessage.conversation_id == conversation_id,
                LiveChatMessage.sender_type.in_([opposite, "system"]),
                LiveChatMessage.is_read == False,
            )
            .update({"is_read": True}, synchronize_session="fetch")
        )
        self.db.commit()
        return updated

    def get_unread_count_for_staff(self) -> int:
        """Đếm tổng tin nhắn customer chưa đọc (hiển thị badge)"""
        return (
            self.db.query(LiveChatMessage)
            .join(LiveChatConversation)
            .filter(
                LiveChatConversation.status.in_(["waiting", "active"]),
                LiveChatMessage.sender_type == "customer",
                LiveChatMessage.is_read == False,
            )
            .count()
        )

    def get_waiting_count(self) -> int:
        """Đếm cuộc hội thoại đang chờ"""
        return (
            self.db.query(LiveChatConversation)
            .filter(LiveChatConversation.status == "waiting")
            .count()
        )

    # ─────────────── PRIVATE ───────────────

    def _get_conversation(self, conversation_id: int) -> Optional[LiveChatConversation]:
        """Lấy cuộc hội thoại theo ID"""
        return (
            self.db.query(LiveChatConversation)
            .filter(LiveChatConversation.conversation_id == conversation_id)
            .first()
        )
