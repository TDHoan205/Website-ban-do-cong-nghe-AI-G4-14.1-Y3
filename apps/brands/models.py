"""
Models cho app brands.
Map với bảng Brands từ SQL Server.
"""
from django.db import models


class Brand(models.Model):
    """
    Thương hiệu - bảng Brands.
    """
    brand_id = models.AutoField(primary_key=True)
    name = models.CharField('Tên thương hiệu', max_length=255, unique=True)
    slug = models.SlugField('Slug', max_length=255, unique=True, blank=True)
    description = models.TextField('Mô tả', blank=True, null=True)
    logo_url = models.CharField('URL logo', max_length=500, blank=True, null=True)
    website = models.URLField('Website', max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Hoạt động', default=True)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)

    class Meta:
        db_table = 'Brands'
        verbose_name = 'Thương hiệu'
        verbose_name_plural = 'Thương hiệu'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return self.products.count()

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
