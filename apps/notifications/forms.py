"""
Forms cho app notifications.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML

from .models import Notification


class NotificationForm(forms.ModelForm):
    """Form tạo thông báo."""

    TYPE_CHOICES = [
        ('Order', 'Thông báo đơn hàng'),
        ('Payment', 'Thanh toán'),
        ('Chat', 'Chat'),
        ('System', 'Hệ thống'),
        ('Promotion', 'Khuyến mãi'),
    ]

    type = forms.ChoiceField(
        label='Loại thông báo',
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Notification
        fields = ['type', 'title', 'message', 'link']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề thông báo',
                'maxlength': '255'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Nhập nội dung thông báo'
            }),
            'link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://techshop.com/orders/ (tùy chọn)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('type', css_class='col-md-6'),
            ),
            'title',
            'message',
            'link',
            Submit('submit', 'Gửi thông báo', css_class='btn-primary'),
            HTML('<a href="/notifications/" class="btn btn-secondary ms-2">Hủy</a>')
        )
