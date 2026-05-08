"""
Models cho app settings.
Quản lý cài đặt website.
"""
from django.db import models


class SiteSetting(models.Model):
    """
    Cài đặt website - lưu trữ key-value settings.
    """
    SETTING_TYPES = [
        ('text', 'Văn bản'),
        ('number', 'Số'),
        ('boolean', 'Boolean'),
        ('image', 'Hình ảnh'),
        ('json', 'JSON'),
    ]

    SETTING_CATEGORIES = [
        ('general', 'Chung'),
        ('contact', 'Liên hệ'),
        ('social', 'Mạng xã hội'),
        ('email', 'Email'),
        ('payment', 'Thanh toán'),
        ('seo', 'SEO'),
        ('other', 'Khác'),
    ]

    setting_id = models.AutoField(primary_key=True)
    key = models.CharField('Key', max_length=100, unique=True,
                          help_text='Tên biến cài đặt (không dấu, gạch dưới)')
    value = models.TextField('Giá trị', blank=True, null=True)
    setting_type = models.CharField('Loại', max_length=20, choices=SETTING_TYPES, default='text')
    category = models.CharField('Danh mục', max_length=20, choices=SETTING_CATEGORIES, default='general')
    description = models.CharField('Mô tả', max_length=255, blank=True)
    is_public = models.BooleanField('Hiển thị công khai', default=False,
                                    help_text='Cho phép hiển thị ở frontend')
    updated_at = models.DateTimeField('Cập nhật', auto_now=True)

    class Meta:
        db_table = 'SiteSettings'
        verbose_name = 'Cài đặt'
        verbose_name_plural = 'Cài đặt'
        ordering = ['category', 'key']

    def __str__(self):
        return f"{self.key} = {self.value[:50]}"

    @classmethod
    def get_setting(cls, key, default=None):
        """Lấy giá trị setting theo key."""
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default

    @classmethod
    def set_setting(cls, key, value, setting_type='text', category='general', description=''):
        """Set giá trị setting."""
        obj, created = cls.objects.update_or_create(
            key=key,
            defaults={
                'value': str(value),
                'setting_type': setting_type,
                'category': category,
                'description': description
            }
        )
        return obj

    def get_typed_value(self):
        """Lấy giá trị theo đúng type."""
        if self.setting_type == 'number':
            try:
                return float(self.value) if '.' in self.value else int(self.value)
            except (ValueError, TypeError):
                return 0
        elif self.setting_type == 'boolean':
            return self.value in ['true', 'True', '1', 'yes', 'Yes']
        elif self.setting_type == 'json':
            import json
            try:
                return json.loads(self.value) if self.value else {}
            except json.JSONDecodeError:
                return {}
        return self.value


class MaintenanceMode(models.Model):
    """Chế độ bảo trì."""
    is_enabled = models.BooleanField('Bật chế độ bảo trì', default=False)
    message = models.TextField('Thông báo', default='Website đang được bảo trì. Vui lòng quay lại sau.')
    allowed_ips = models.TextField('IP được phép truy cập', blank=True,
                                  help_text='Mỗi IP trên 1 dòng')
    updated_at = models.DateTimeField('Cập nhật', auto_now=True)

    class Meta:
        db_table = 'MaintenanceMode'

    def __str__(self):
        return f"Bảo trì: {'Bật' if self.is_enabled else 'Tắt'}"
