"""
Models cho app reviews.
Map với bảng Reviews từ SQL Server.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.users.models import Account
from apps.products.models import Product


class Review(models.Model):
    """
    Đánh giá sản phẩm - bảng Reviews.
    """
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_column='product_id'
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviews',
        db_column='account_id'
    )
    rating = models.IntegerField(
        'Đánh giá (1-5)',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    title = models.CharField('Tiêu đề', max_length=255, blank=True, null=True)
    comment = models.TextField('Bình luận', blank=True, null=True)
    is_approved = models.BooleanField('Đã duyệt', default=False)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)

    class Meta:
        db_table = 'Reviews'
        verbose_name = 'Đánh giá'
        verbose_name_plural = 'Đánh giá'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.account} - {self.product} ({self.rating}★)"

    @property
    def rating_stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)
