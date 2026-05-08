"""
Models cho app faqs.
Map với bảng FAQs từ SQL Server.
"""
from django.db import models


class FAQ(models.Model):
    """
    FAQ - Câu hỏi thường gặp - bảng FAQs.
    """
    CATEGORY_CHOICES = [
        ('General', 'Câu hỏi chung'),
        ('Order', 'Về đơn hàng'),
        ('Payment', 'Thanh toán'),
        ('Shipping', 'Vận chuyển'),
        ('Return', 'Đổi trả'),
        ('Product', 'Sản phẩm'),
    ]

    faq_id = models.AutoField(primary_key=True)
    question = models.TextField('Câu hỏi')
    answer = models.TextField('Câu trả lời')
    category = models.CharField('Danh mục', max_length=50, choices=CATEGORY_CHOICES, default='General')
    keywords = models.TextField('Từ khóa', blank=True, null=True,
                               help_text='Các từ khóa liên quan, cách nhau bởi dấu phẩy')
    priority = models.IntegerField('Độ ưu tiên', default=0,
                                    help_text='Số càng lớn càng ưu tiên hiển thị')
    is_active = models.BooleanField('Hoạt động', default=True)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)

    class Meta:
        db_table = 'FAQs'
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.question[:100]

    def get_keywords_list(self):
        if not self.keywords:
            return []
        return [kw.strip() for kw in self.keywords.split(',') if kw.strip()]
