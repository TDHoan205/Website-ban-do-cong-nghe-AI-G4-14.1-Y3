"""
Forms cho app accounts.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div, Fieldset
from crispy_forms.bootstrap import FormActions

from .models import Account, Employee


class LoginForm(forms.Form):
    """Form đăng nhập."""
    username = forms.CharField(
        label='Tên đăng nhập',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập tên đăng nhập',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập mật khẩu'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            FormActions(
                Submit('submit', 'Đăng nhập', css_class='btn-primary w-100')
            )
        )


class AccountForm(forms.ModelForm):
    """Form tài khoản - gộp thông tin Account và Employee."""
    
    # Employee fields (only used for Employee role)
    employee_code = forms.CharField(
        label='Mã nhân viên',
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'VD: NV001'
        })
    )
    department = forms.CharField(
        label='Phòng ban',
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'VD: Kinh doanh'
        })
    )
    position = forms.CharField(
        label='Chức vụ',
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'VD: Nhân viên'
        })
    )
    hire_date = forms.DateField(
        label='Ngày vào làm',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    salary = forms.IntegerField(
        label='Lương',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'VD: 10000000'
        })
    )
    password = forms.CharField(
        label='Mật khẩu',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Để trống nếu không đổi mật khẩu'
        })
    )
    password_confirm = forms.CharField(
        label='Xác nhận mật khẩu',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập lại mật khẩu'
        })
    )

    class Meta:
        model = Account
        fields = ['username', 'email', 'full_name', 'phone', 'address', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên đăng nhập'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Họ và tên'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số điện thoại'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Địa chỉ'
            }),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        cancel_url = reverse('accounts:account_list')
        
        # If editing, populate employee fields
        if self.instance and self.instance.pk:
            try:
                employee = self.instance.employee_profile
                self.fields['employee_code'].initial = employee.employee_code
                self.fields['department'].initial = employee.department
                self.fields['position'].initial = employee.position
                self.fields['hire_date'].initial = employee.hire_date
                self.fields['salary'].initial = employee.salary
            except Employee.DoesNotExist:
                pass
        
        self.helper.layout = Layout(
            Fieldset(
                'Thông tin đăng nhập',
                Row(
                    Column('username', css_class='col-md-6'),
                    Column('email', css_class='col-md-6'),
                ),
                Row(
                    Column('password', css_class='col-md-6'),
                    Column('password_confirm', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Thông tin cá nhân',
                Row(
                    Column('full_name', css_class='col-md-6'),
                    Column('phone', css_class='col-md-6'),
                ),
                'address',
                Row(
                    Column('role', css_class='col-md-4'),
                    Column('is_active', css_class='col-md-4 d-flex align-items-center'),
                ),
            ),
            Fieldset(
                'Thông tin nhân viên',
                Row(
                    Column('employee_code', css_class='col-md-6'),
                    Column('department', css_class='col-md-6'),
                ),
                Row(
                    Column('position', css_class='col-md-6'),
                    Column('hire_date', css_class='col-md-6'),
                ),
                'salary',
                css_id='employee_fields',
            ),
            FormActions(
                Submit('submit', 'Lưu', css_class='btn-primary me-2'),
                HTML(f'<a href="{cancel_url}" class="btn btn-secondary">Hủy</a>')
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        role = cleaned_data.get('role')

        # Validate password only if provided
        if password or password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('Mật khẩu xác nhận không khớp!')
            if len(password) < 6:
                raise forms.ValidationError('Mật khẩu phải có ít nhất 6 ký tự!')

        # Validate employee fields only if role is Employee
        if role == 'Employee':
            employee_code = cleaned_data.get('employee_code')
            if not employee_code:
                self.add_error('employee_code', 'Mã nhân viên là bắt buộc cho nhân viên!')

        return cleaned_data

    def save(self, commit=True):
        account = super().save(commit=False)
        
        # Handle password
        password = self.cleaned_data.get('password')
        if password:
            account.set_password(password)
        
        if commit:
            account.save()
            
            # Save employee info if role is Employee
            if account.role == 'Employee':
                employee, created = Employee.objects.get_or_create(
                    account=account,
                    defaults={
                        'employee_code': self.cleaned_data.get('employee_code', f'NV{account.pk or "NEW"}'),
                        'department': self.cleaned_data.get('department', ''),
                        'position': self.cleaned_data.get('position', ''),
                        'hire_date': self.cleaned_data.get('hire_date'),
                        'salary': self.cleaned_data.get('salary'),
                    }
                )
                if not created:
                    employee.employee_code = self.cleaned_data.get('employee_code', employee.employee_code)
                    employee.department = self.cleaned_data.get('department', employee.department)
                    employee.position = self.cleaned_data.get('position', employee.position)
                    employee.hire_date = self.cleaned_data.get('hire_date', employee.hire_date)
                    employee.salary = self.cleaned_data.get('salary', employee.salary)
                    employee.save()
        
        return account


class EmployeeForm(forms.ModelForm):
    """Form nhân viên (legacy - giữ lại để tương thích ngược)."""

    class Meta:
        model = Employee
        fields = ['employee_code', 'department', 'position', 'hire_date', 'salary', 'is_active']
        widgets = {
            'employee_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mã nhân viên (VD: NV-001)'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phòng ban'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Chức vụ'
            }),
            'hire_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lương'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        cancel_url = reverse('accounts:employee_list')
        self.helper.layout = Layout(
            Row(
                Column('employee_code', css_class='col-md-6'),
                Column('department', css_class='col-md-6'),
            ),
            Row(
                Column('position', css_class='col-md-6'),
                Column('hire_date', css_class='col-md-6'),
            ),
            'salary',
            'is_active',
            FormActions(
                Submit('submit', 'Lưu', css_class='btn-primary'),
                HTML(f'<a href="{cancel_url}" class="btn btn-secondary">Hủy</a>')
            )
        )


class ProfileForm(forms.ModelForm):
    """Form thông tin cá nhân."""

    class Meta:
        model = Account
        fields = ['email', 'full_name', 'phone', 'address']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Họ và tên'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số điện thoại'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Địa chỉ'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'email',
            'full_name',
            'phone',
            'address',
            FormActions(
                Submit('submit', 'Cập nhật', css_class='btn-primary')
            )
        )


class RegisterForm(forms.ModelForm):
    """Form đăng ký tài khoản mới."""
    password1 = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(attrs={
            'class': 'input-with-icon',
            'placeholder': 'Mật khẩu (tối thiểu 6 ký tự)'
        }),
        min_length=6
    )

    class Meta:
        model = Account
        fields = ['username', 'full_name', 'email', 'phone', 'address']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-with-icon',
                'placeholder': 'Tên đăng nhập'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'input-with-icon',
                'placeholder': 'Họ và tên'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-with-icon',
                'placeholder': 'Email (không bắt buộc)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input-with-icon',
                'placeholder': 'Số điện thoại'
            }),
            'address': forms.TextInput(attrs={
                'class': 'input-with-icon',
                'placeholder': 'Địa chỉ (không bắt buộc)'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        if password1 and len(password1) < 6:
            self.add_error('password1', 'Mật khẩu phải có ít nhất 6 ký tự!')
        return cleaned_data

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data['password1'])
        account.role = 'Customer'  # Mặc định là Customer
        if commit:
            account.save()
        return account


class ForgotPasswordForm(forms.Form):
    """Form quên mật khẩu."""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'input-with-icon',
            'placeholder': 'Nhập địa chỉ email của bạn'
        })
    )
