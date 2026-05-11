"""
Models cho app orders.
Map voi bang Orders, OrderItems, OrderStatusHistory tu SQL Server.
"""
from django.db import models
from django.core.validators import MinValueValidator

from apps.users.models import Account
from apps.products.models import Product, ProductVariant


class Order(models.Model):
    """
    Don hang - bang Orders.
    Ho tro ca guest (account=None) va member (account=Account).
    """
    STATUS_CHOICES = [
        ('Pending', 'Cho xac nhan'),
        ('Confirmed', 'Da xac nhan'),
        ('Processing', 'Dang xu ly'),
        ('Shipped', 'Dang giao hang'),
        ('Delivered', 'Da giao hang'),
        ('Cancelled', 'Da huy'),
        ('Returned', 'Tra hang'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'COD (Nhan hang tra tien)'),
        ('VNPAY', 'VNPAY'),
        ('BANK_TRANSFER', 'Chuyen khoan ngan hang'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Chua thanh toan'),
        ('AwaitingConfirmation', 'Cho xac nhan'),
        ('Paid', 'Da thanh toan'),
        ('Failed', 'That bai'),
    ]

    order_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        db_column='account_id'
    )
    order_code = models.CharField('Ma don hang', max_length=50, unique=True)
    order_date = models.DateTimeField('Ngay dat', auto_now_add=True)
    total_amount = models.DecimalField('Tong tien', max_digits=12, decimal_places=2)
    shipping_fee = models.DecimalField('Phi ship', max_digits=10, decimal_places=2, default=0)
    status = models.CharField('Trang thai', max_length=20, choices=STATUS_CHOICES, default='Pending')
    customer_name = models.CharField('Ten khach hang', max_length=100, blank=True, null=True)
    customer_phone = models.CharField('So dien thoai', max_length=20, blank=True, null=True)
    customer_address = models.CharField('Dia chi', max_length=255, blank=True, null=True)
    notes = models.TextField('Ghi chu', blank=True, null=True)
    admin_notes = models.TextField('Ghi chu admin', blank=True, null=True)
    shipping_method = models.CharField('Phuong thuc van chuyen', max_length=50, blank=True, null=True)
    tracking_number = models.CharField('Ma van don', max_length=100, blank=True, null=True)
    payment_method = models.CharField(
        'Phuong thuc thanh toan',
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='COD',
    )
    payment_status = models.CharField(
        'Trang thai thanh toan',
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending',
    )
    vnpay_transaction_id = models.CharField('Ma GD VNPAY', max_length=100, blank=True, null=True)
    estimated_delivery = models.DateField('Du kien giao', blank=True, null=True)
    created_at = models.DateTimeField('Ngay tao', auto_now_add=True)
    updated_at = models.DateTimeField('Ngay cap nhat', auto_now=True)

    class Meta:
        db_table = 'Orders'
        verbose_name = 'Don hang'
        verbose_name_plural = 'Don hang'
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

    @property
    def payment_status_display(self):
        return dict(self.PAYMENT_STATUS_CHOICES).get(self.payment_status, self.payment_status)

    @property
    def final_amount(self):
        return self.total_amount + (self.shipping_fee or 0)


class OrderItem(models.Model):
    """
    Item trong don hang - bang OrderItems.
    Luu tru product_name/variant_name de dam bao hien thi dung ngay ca khi san pham bi xoa.
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
    product_name = models.CharField('Ten san pham', max_length=255)
    variant_name = models.CharField('Ten bien the', max_length=100, blank=True, null=True)
    quantity = models.IntegerField('So luong', validators=[MinValueValidator(1)])
    unit_price = models.DecimalField('Don gia', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField('Thanh tien', max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'OrderItems'
        verbose_name = 'Chi tiet don hang'
        verbose_name_plural = 'Chi tiet don hang'

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    """
    Lich su trang thai don hang - bang OrderStatusHistory.
    Theo doi moi thay doi trang thai cua don hang.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history',
        db_column='order_id'
    )
    old_status = models.CharField('Trang thai cu', max_length=20, blank=True, null=True)
    new_status = models.CharField('Trang thai moi', max_length=20)
    changed_by = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='status_changes',
        db_column='changed_by_id'
    )
    notes = models.TextField('Ghi chu', blank=True, null=True)
    created_at = models.DateTimeField('Thoi gian', auto_now_add=True)

    class Meta:
        db_table = 'OrderStatusHistory'
        verbose_name = 'Lich su trang thai'
        verbose_name_plural = 'Lich su trang thai'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order.order_code}: {self.old_status} -> {self.new_status}"
