"""
Models cho app suppliers.
Map với bảng Suppliers từ SQL Server.
"""
from django.db import models


class Supplier(models.Model):
    """
    Nhà cung cấp - bảng Suppliers.
    """
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField('Tên nhà cung cấp', max_length=255)
    contact_person = models.CharField('Người liên hệ', max_length=100, blank=True, null=True)
    phone = models.CharField('Số điện thoại', max_length=20, blank=True, null=True)
    email = models.EmailField('Email', max_length=100, blank=True, null=True)
    address = models.CharField('Địa chỉ', max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Hoạt động', default=True)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)

    class Meta:
        db_table = 'Suppliers'
        verbose_name = 'Nhà cung cấp'
        verbose_name_plural = 'Nhà cung cấp'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return self.products.count()
