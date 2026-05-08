"""
Models cho app notifications.
Map với bảng Notifications từ SQL Server.
"""
from django.db import models

from apps.users.models import Account


class Notification(models.Model):
    """
    Thông báo - bảng Notifications.
    """
    TYPE_CHOICES = [
        ('Order', 'Thông báo đơn hàng'),
        ('Payment', 'Thanh toán'),
        ('Chat', 'Chat'),
        ('System', 'Hệ thống'),
        ('Promotion', 'Khuyến mãi'),
    ]

    notification_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        db_column='account_id'
    )
    type = models.CharField('Loại', max_length=50, choices=TYPE_CHOICES, default='System')
    title = models.CharField('Tiêu đề', max_length=255)
    message = models.TextField('Nội dung')
    is_read = models.BooleanField('Đã đọc', default=False)
    link = models.CharField('Link', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField('Thời gian', auto_now_add=True)

    class Meta:
        db_table = 'Notifications'
        verbose_name = 'Thông báo'
        verbose_name_plural = 'Thông báo'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


    @classmethod
    def create_notification(cls, account, notification_type, title, message, link=None):
        """Tạo thông báo mới."""
        return cls.objects.create(
            account=account,
            type=notification_type,
            title=title,
            message=message,
            link=link
        )
