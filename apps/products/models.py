"""
Models cho app products.
Map với bảng Products, ProductVariants, ProductImages từ SQL Server.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.categories.models import Category
from apps.suppliers.models import Supplier


class Product(models.Model):
    """
    Sản phẩm - bảng Products.
    """
    product_id = models.AutoField(primary_key=True)
    name = models.CharField('Tên sản phẩm', max_length=255)
    description = models.TextField('Mô tả', blank=True, null=True)
    image_url = models.CharField('URL hình ảnh', max_length=500, blank=True, null=True)
    price = models.DecimalField('Giá bán', max_digits=10, decimal_places=2)
    original_price = models.DecimalField('Giá gốc', max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.IntegerField('Số lượng tồn', default=0)
    is_available = models.BooleanField('Còn hàng', default=True)
    rating = models.DecimalField('Đánh giá', max_digits=2, decimal_places=1, default=4.5,
                                validators=[MinValueValidator(0), MaxValueValidator(5)])
    is_new = models.BooleanField('Sản phẩm mới', default=False)
    is_hot = models.BooleanField('Sản phẩm hot', default=False)
    discount_percent = models.IntegerField('Giảm giá (%)', default=0,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    specifications = models.TextField('Thông số kỹ thuật', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        db_column='category_id'
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        db_column='supplier_id'
    )
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)

    class Meta:
        db_table = 'Products'
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_deal(self):
        """Kiểm tra có đang giảm giá không."""
        return self.discount_percent > 0 or (
            self.original_price is not None and self.original_price > self.price
        )

    @property
    def sale_price(self):
        """Tính giá sau giảm."""
        if self.discount_percent > 0:
            return self.price * (100 - self.discount_percent) / 100
        return self.price

    @property
    def variant_count(self):
        return self.variants.count()


class ProductVariant(models.Model):
    """
    Biến thể sản phẩm - bảng ProductVariants.
    """
    variant_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        db_column='product_id'
    )
    color = models.CharField('Màu sắc', max_length=50, blank=True, null=True)
    storage = models.CharField('Dung lượng', max_length=20, blank=True, null=True)
    ram = models.CharField('RAM', max_length=20, blank=True, null=True)
    variant_name = models.CharField('Tên biến thể', max_length=100)
    sku = models.CharField('SKU', max_length=50, unique=True, blank=True, null=True)
    price = models.DecimalField('Giá', max_digits=10, decimal_places=2, blank=True, null=True)
    original_price = models.DecimalField('Giá gốc', max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.IntegerField('Số lượng tồn', default=0)
    display_order = models.IntegerField('Thứ tự hiển thị', default=0)
    is_active = models.BooleanField('Hoạt động', default=True)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)

    class Meta:
        db_table = 'ProductVariants'
        verbose_name = 'Biến thể'
        verbose_name_plural = 'Biến thể'
        ordering = ['display_order', 'variant_name']

    def __str__(self):
        return self.variant_name

    @property
    def effective_price(self):
        """Giá thực tế (ưu tiên price của variant, không có thì lấy của product)."""
        return self.price if self.price else self.product.price


class ProductImage(models.Model):
    """
    Hình ảnh sản phẩm - bảng ProductImages.
    Hỗ trợ nhiều ảnh theo sản phẩm và theo biến thể.
    """
    image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images',
        db_column='product_id'
    )
    variant = models.ForeignKey(
        'ProductVariant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='images',
        db_column='variant_id'
    )
    image_url = models.CharField('URL hình ảnh', max_length=500)
    display_order = models.IntegerField('Thứ tự hiển thị', default=0)
    is_primary = models.BooleanField('Hình chính', default=False)
    is_thumbnail = models.BooleanField('Hình thu nhỏ', default=False)
    alt_text = models.CharField('Alt text', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)

    class Meta:
        db_table = 'ProductImages'
        verbose_name = 'Hình ảnh'
        verbose_name_plural = 'Hình ảnh'
        ordering = ['display_order', '-is_primary', '-image_id']

    def __str__(self):
        return f"{self.product.name} - Image {self.image_id}"
