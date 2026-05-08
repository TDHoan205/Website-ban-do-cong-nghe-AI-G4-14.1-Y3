"""
Models cho app slides.
Map với bảng Slides từ SQL Server.
"""
from django.db import models


class Slide(models.Model):
    """
    Slide banner - bảng Slides.
    """
    slide_id = models.AutoField(primary_key=True)
    title = models.CharField('Tiêu đề', max_length=255)
    subtitle = models.CharField('Phụ đề', max_length=255, blank=True, null=True)
    image_url = models.CharField('URL hình ảnh', max_length=500)
    link = models.CharField('Link liên kết', max_length=255, blank=True, null=True)
    button_text = models.CharField('Text nút bấm', max_length=50, blank=True, null=True)
    display_order = models.IntegerField('Thứ tự hiển thị', default=0)
    is_active = models.BooleanField('Hoạt động', default=True)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)

    class Meta:
        db_table = 'Slides'
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides'
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title
