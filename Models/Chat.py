"""
Chat Models - AI Chatbot
Tương đương Models/AI/Chat/Entities/ trong C#
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class ChatSession(Base):
    __tablename__ = "ChatSessions"

    session_id = Column(Integer, primary_key=True, index=True)
    session_uuid = Column(String(36), unique=True, nullable=False)
    account_id = Column(Integer, ForeignKey("Accounts.account_id"), nullable=True)
    device_info = Column(String(255))
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)

    account = relationship("Account")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ChatSession(uuid='{self.session_uuid}')>"


class ChatMessage(Base):
    __tablename__ = "ChatMessages"

    message_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("ChatSessions.session_id"), nullable=False)
    sender_type = Column(String(20), nullable=False)  # 'user', 'bot', 'staff'
    message_content = Column(Text, nullable=False)
    intent = Column(String(50))  # product_query, order_status, general, etc.
    confidence_score = Column(String(10))
    is_product_recommendation = Column(Boolean, default=False)
    recommended_product_ids = Column(String(255))  # JSON array of product IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ChatSession", back_populates="messages")

    def __repr__(self):
        return f"<ChatMessage(sender='{self.sender_type}')>"


class AIConversationLog(Base):
    __tablename__ = "AIConversationLogs"

    log_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("ChatSessions.session_id"), nullable=False)
    account_id = Column(Integer, ForeignKey("Accounts.account_id"), nullable=True)
    user_message = Column(Text)
    bot_response = Column(Text)
    intent_detected = Column(String(50))
    confidence_score = Column(String(10))
    response_time_ms = Column(Integer)
    is_escalated_to_staff = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ChatSession")
    account = relationship("Account")

    def __repr__(self):
        return f"<AIConversationLog(session_id={self.session_id})>"


class FAQ(Base):
    __tablename__ = "FAQs"

    faq_id = Column(Integer, primary_key=True, index=True)
    question = Column(String(500), nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(50))
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<FAQ(question='{self.question[:50]}...')>"


class Notification(Base):
    __tablename__ = "Notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("Accounts.account_id"), nullable=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    notification_type = Column(String(50))  # order_update, promotion, system
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("Account")

    def __repr__(self):
        return f"<Notification(title='{self.title}')>"


"""
Knowledge Models - AI Knowledge Base
"""


class KnowledgeChunk(Base):
    __tablename__ = "KnowledgeChunks"

    chunk_id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    content_type = Column(String(50))  # product_info, faq, policy
    source_id = Column(Integer)  # Reference to source entity
    source_table = Column(String(50))  # Table name
    embedding_vector = Column(Text)  # Vector embedding
    metadata_json = Column(Text)  # JSON metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<KnowledgeChunk(type='{self.content_type}')>"
