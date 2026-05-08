"""
Models cho app orders.
Map với bảng Orders, OrderItems từ SQL Server.
"""
from django.db import models
from django.core.validators import MinValueValidator

from apps.users.models import Account
from apps.products.models import Product, ProductVariant


class Order(models.Model):
    """
    Đơn hàng - bảng Orders.
    """
    STATUS_CHOICES = [
        ('Pending', 'Chờ xác nhận'),
        ('Confirmed', 'Đã xác nhận'),
        ('Processing', 'Đang xử lý'),
        ('Shipped', 'Đang giao hàng'),
        ('Delivered', 'Đã giao hàng'),
        ('Cancelled', 'Đã hủy'),
        ('Returned', 'Trả hàng'),
    ]

    order_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        db_column='account_id'
    )
    order_code = models.CharField('Mã đơn hàng', max_length=50, unique=True)
    order_date = models.DateTimeField('Ngày đặt', auto_now_add=True)
    total_amount = models.DecimalField('Tổng tiền', max_digits=12, decimal_places=2)
    status = models.CharField('Trạng thái', max_length=20, choices=STATUS_CHOICES, default='Pending')
    customer_name = models.CharField('Tên khách hàng', max_length=100, blank=True, null=True)
    customer_phone = models.CharField('Số điện thoại', max_length=20, blank=True, null=True)
    customer_address = models.CharField('Địa chỉ', max_length=255, blank=True, null=True)
    notes = models.TextField('Ghi chú', blank=True, null=True)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)

    class Meta:
        db_table = 'Orders'
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
        ordering = ['-order_date']

    def __str__(self):
        return self.order_code

    def save(self, *args, **kwargs):
        if not self.order_code:
            from django.utils import timezone
            self.order_code = f"ORD{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    @property
    def item_count(self):
        return self.items.count()

    @property
    def can_cancel(self):
        return self.status in ['Pending', 'Confirmed']

    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class OrderItem(models.Model):
    """
    Item trong đơn hàng - bảng OrderItems.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        db_column='order_id'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        db_column='product_id'
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items',
        db_column='variant_id'
    )
    product_name = models.CharField('Tên sản phẩm', max_length=255)
    variant_name = models.CharField('Tên biến thể', max_length=100, blank=True, null=True)
    quantity = models.IntegerField('Số lượng', validators=[MinValueValidator(1)])
    unit_price = models.DecimalField('Đơn giá', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField('Thành tiền', max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'OrderItems'
        verbose_name = 'Chi tiết đơn hàng'
        verbose_name_plural = 'Chi tiết đơn hàng'

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
