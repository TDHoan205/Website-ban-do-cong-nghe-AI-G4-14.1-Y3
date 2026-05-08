"""
Models cho app accounts.
Map với bảng Accounts, Employees từ SQL Server.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class AccountManager(BaseUserManager):
    """Custom manager cho Account model."""

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username là bắt buộc')
        account = self.model(username=username, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'Admin')
        return self.create_user(username, password, **extra_fields)


class Account(AbstractBaseUser):
    """
    Tài khoản người dùng - bảng Accounts.
    Sử dụng custom user model.
    """
    account_id = models.AutoField(primary_key=True)
    username = models.CharField('Tên đăng nhập', max_length=50, unique=True, db_index=True)
    password_hash = models.CharField('Mật khẩu', max_length=255)
    email = models.EmailField('Email', max_length=100, unique=True, blank=True, null=True)
    full_name = models.CharField('Họ tên', max_length=100, blank=True, null=True)
    phone = models.CharField('Số điện thoại', max_length=20, blank=True, null=True)
    address = models.CharField('Địa chỉ', max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Hoạt động', default=True)
    role = models.CharField(
        'Vai trò',
        max_length=20,
        choices=[
            ('Admin', 'Quản trị viên'),
            ('Employee', 'Nhân viên'),
            ('Customer', 'Khách hàng'),
        ],
        default='Customer'
    )
    reset_token = models.CharField('Token reset', max_length=64, blank=True, null=True)
    reset_token_expiry = models.DateTimeField('Hết hạn token', blank=True, null=True)
    is_staff = models.BooleanField('Staff', default=False)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'Accounts'
        verbose_name = 'Tài khoản'
        verbose_name_plural = 'Tài khoản'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'Admin'

    @property
    def is_employee(self):
        return self.role in ['Admin', 'Employee']

    def has_module_perms(self, app_label):
        """Kiểm tra quyền truy cập module."""
        return self.is_active and self.is_employee

    def has_perm(self, perm, obj=None):
        """Kiểm tra quyền."""
        return self.is_active and self.is_employee

    def has_perms(self, perm_list, obj=None):
        """Kiểm tra quyền."""
        return self.is_active and self.is_employee


class Employee(models.Model):
    """
    Nhân viên - bảng Employees.
    Liên kết 1-1 với Account.
    """
    employee_id = models.AutoField(primary_key=True)
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        db_column='account_id'
    )
    employee_code = models.CharField('Mã nhân viên', max_length=10, unique=True)
    department = models.CharField('Phòng ban', max_length=50, blank=True, null=True)
    position = models.CharField('Chức vụ', max_length=50, blank=True, null=True)
    hire_date = models.DateField('Ngày vào làm', blank=True, null=True)
    salary = models.IntegerField('Lương', blank=True, null=True)
    is_active = models.BooleanField('Hoạt động', default=True)
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)

    class Meta:
        db_table = 'Employees'
        verbose_name = 'Nhân viên'
        verbose_name_plural = 'Nhân viên'

    def __str__(self):
        return f"{self.employee_code} - {self.account.full_name if self.account.full_name else self.account.username}"
