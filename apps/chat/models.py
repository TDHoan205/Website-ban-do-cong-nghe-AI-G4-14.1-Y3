"""
Models cho app chat.
Map với bảng ChatSessions, ChatMessages, AIConversationLogs từ SQL Server.
"""
from django.db import models
import uuid

from apps.users.models import Account


class ChatSession(models.Model):
    """
    Phiên chat - bảng ChatSessions.
    """
    STATUS_CHOICES = [
        ('Active', 'Đang chat'),
        ('Waiting', 'Đang chờ'),
        ('Closed', 'Đã đóng'),
    ]

    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='chat_sessions',
        null=True,
        blank=True,
        db_column='account_id'
    )
    status = models.CharField('Trạng thái', max_length=20, choices=STATUS_CHOICES, default='Waiting')
    assigned_to = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_chats',
        db_column='assigned_to'
    )
    started_at = models.DateTimeField('Bắt đầu', auto_now_add=True)
    ended_at = models.DateTimeField('Kết thúc', null=True, blank=True)

    class Meta:
        db_table = 'ChatSessions'
        verbose_name = 'Phiên chat'
        verbose_name_plural = 'Phiên chat'
        ordering = ['-started_at']

    def __str__(self):
        return f"Session {self.session_id}"

    @property
    def message_count(self):
        return self.messages.count()

    @property
    def duration_minutes(self):
        if self.ended_at:
            delta = self.ended_at - self.started_at
            return int(delta.total_seconds() / 60)
        return None


class ChatMessage(models.Model):
    """
    Tin nhắn chat - bảng ChatMessages.
    """
    SENDER_CHOICES = [
        ('user', 'Khách hàng'),
        ('admin', 'Nhân viên'),
        ('bot', 'Bot'),
    ]

    message_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        db_column='session_id'
    )
    message = models.TextField('Nội dung')
    sender_type = models.CharField('Người gửi', max_length=10, choices=SENDER_CHOICES)
    sender = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_messages'
    )
    created_at = models.DateTimeField('Thời gian', auto_now_add=True)
    metadata = models.JSONField('Metadata', null=True, blank=True)

    class Meta:
        db_table = 'ChatMessages'
        verbose_name = 'Tin nhắn'
        verbose_name_plural = 'Tin nhắn'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender_type}: {self.message[:50]}"


class AIConversationLog(models.Model):
    """
    Log hội thoại AI - bảng AIConversationLogs.
    """
    log_id = models.AutoField(primary_key=True)
    session_id = models.UUIDField('Session ID')
    user_message = models.TextField('Tin nhắn user')
    ai_response = models.TextField('Phản hồi AI')
    intent_detected = models.CharField('Intent phát hiện', max_length=50, null=True, blank=True)
    confidence_score = models.DecimalField('Độ chính xác', max_digits=5, decimal_places=2, null=True, blank=True)
    was_escalated = models.BooleanField('Được chuyển sang nhân viên', default=False)
    user_rating = models.IntegerField('Đánh giá', null=True, blank=True)
    created_at = models.DateTimeField('Thời gian', auto_now_add=True)

    class Meta:
        db_table = 'AIConversationLogs'
        verbose_name = 'Log AI'
        verbose_name_plural = 'Log AI'
        ordering = ['-created_at']

    def __str__(self):
        return f"Log {self.log_id} - {self.intent_detected}"
