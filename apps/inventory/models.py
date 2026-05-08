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
        Cập nhật số lượng tồn kho.
        
        Args:
            quantity_change: Số lượng thay đổi (dương = nhập kho, âm = xuất kho)
            movement_type: Loại biến động (manual, order, return)
            notes: Ghi chú thêm
        """
        self.stock_quantity += quantity_change
        if self.stock_quantity < 0:
            self.stock_quantity = 0
        self.save()
        
        # Log movement (có thể tạo thêm InventoryMovement model)
        return self.stock_quantity
