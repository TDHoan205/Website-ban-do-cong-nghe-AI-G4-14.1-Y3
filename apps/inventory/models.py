"""
Models cho app inventory.
Map với bảng Inventory từ SQL Server.
"""
from django.db import models

from apps.products.models import Product


class Inventory(models.Model):
    """
    Tồn kho - bảng Inventory.
    Theo dõi số lượng tồn kho của sản phẩm.
    """
    inventory_id = models.AutoField(primary_key=True)
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory',
        db_column='product_id'
    )
    stock_quantity = models.IntegerField('Số lượng tồn kho', default=0)
    low_stock_threshold = models.IntegerField('Ngưỡng báo động', default=10)
    last_updated = models.DateTimeField('Cập nhật lần cuối', auto_now=True)
    notes = models.TextField('Ghi chú', blank=True, null=True)

    class Meta:
        db_table = 'Inventory'
        verbose_name = 'Tồn kho'
        verbose_name_plural = 'Tồn kho'

    def __str__(self):
        return f"{self.product.name}: {self.stock_quantity}"

    @property
    def is_low_stock(self):
        """Kiểm tra nếu số lượng tồn dưới ngưỡng."""
        return self.stock_quantity <= self.low_stock_threshold

    @property
    def is_out_of_stock(self):
        """Kiểm tra nếu hết hàng."""
        return self.stock_quantity <= 0

    def update_stock(self, quantity_change, movement_type='manual', notes=None):
        """
        Cap nhat so luong ton kho.

        Args:
            quantity_change: So luong thay doi (duong = nhap kho, am = xuat kho)
            movement_type: Loai bien dong (manual, order, return)
            notes: Ghi chu them
        """
        self.stock_quantity += quantity_change
        if self.stock_quantity < 0:
            self.stock_quantity = 0
        self.save()
        return self.stock_quantity


class InventoryMovement(models.Model):
    """
    Bang theo doi bien dong kho - Nhap/Xuat kho.
    """
    MOVEMENT_TYPES = [
        ('IN', 'Nhap kho'),
        ('OUT', 'Xuat kho'),
        ('ADJUST', 'Dieu chinh'),
        ('RETURN', 'Tra hang'),
    ]

    movement_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory_movements',
        db_column='product_id'
    )
    movement_type = models.CharField(
        'Loai bien dong',
        max_length=20,
        choices=MOVEMENT_TYPES,
    )
    quantity = models.IntegerField('So luong')
    reason = models.CharField('Ly do', max_length=200)
    related_order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory_movements',
        db_column='related_order_id'
    )
    created_by = models.ForeignKey(
        'users.Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory_movements',
        db_column='created_by_id'
    )
    created_at = models.DateTimeField('Thoi gian', auto_now_add=True)

    class Meta:
        db_table = 'InventoryMovements'
        verbose_name = 'Bien dong kho'
        verbose_name_plural = 'Bien dong kho'
        ordering = ['-created_at']

    def __str__(self):
        prefix = '+' if self.movement_type == 'IN' else '-'
        return f"{self.product.name} {prefix}{self.quantity} ({self.movement_type}) - {self.reason}"
