"""
Models cho app cart.
Map với bảng Cart_Items từ SQL Server.
"""
from django.db import models

from apps.users.models import Account
from apps.products.models import Product, ProductVariant


class CartItem(models.Model):
    """
    Item trong giỏ hàng - bảng Cart_Items.
    """
    cart_item_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='cart_items',
        db_column='account_id',
        blank=True,
        null=True,
    )
    session_key = models.CharField(
        'Session key (Guest)',
        max_length=40,
        blank=True,
        null=True,
        db_index=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        db_column='product_id'
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items',
        db_column='variant_id'
    )
    quantity = models.IntegerField('Số lượng', default=1)
    added_date = models.DateTimeField('Ngày thêm', auto_now_add=True)

    class Meta:
        db_table = 'Cart_Items'
        verbose_name = 'Giỏ hàng'
        verbose_name_plural = 'Giỏ hàng'
        unique_together = []  # Checked in clean()

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.account and not self.session_key:
            raise ValidationError('CartItem phai co account hoac session_key.')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def unit_price(self):
        if self.variant and self.variant.price is not None:
            return float(self.variant.price)
        return float(self.product.price or 0)

    @property
    def subtotal(self):
        return float(self.quantity * self.unit_price) if self.unit_price else 0
