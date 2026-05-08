"""
Models cho app categories.
Map với bảng Categories từ SQL Server.
"""
from django.db import models


class Category(models.Model):
    """
    Danh mục sản phẩm - bảng Categories.
    """
    category_id = models.AutoField(primary_key=True)
    name = models.CharField('Tên danh mục', max_length=100, unique=True)
    description = models.TextField('Mô tả', blank=True, null=True)
    image_url = models.CharField('URL hình ảnh', max_length=500, blank=True, null=True)
    display_order = models.IntegerField('Thứ tự hiển thị', default=0)
    is_active = models.BooleanField('Hoạt động', default=True)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)

    icon_name = models.CharField('Tên icon', max_length=50, default='box', help_text='Tên icon Bootstrap Icons, ví dụ: mobile-alt, laptop, headphones')

    class Meta:
        db_table = 'Categories'
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return self.products.count()
