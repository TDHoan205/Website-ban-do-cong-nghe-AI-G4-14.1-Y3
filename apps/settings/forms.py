"""
Forms cho app settings.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import SiteSetting, MaintenanceMode


class SiteSettingForm(forms.ModelForm):
    """Form cài đặt website."""

    class Meta:
        model = SiteSetting
        fields = ['key', 'value', 'setting_type', 'category', 'description', 'is_public']
        widgets = {
            'key': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ví dụ: site_name'
            }),
            'value': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
            'setting_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mô tả ngắn'
            }),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'key',
            'value',
            'description',
            'setting_type',
            'category',
            'is_public',
            Submit('submit', 'Lưu', css_class='btn-primary')
        )


class MaintenanceModeForm(forms.ModelForm):
    """Form chế độ bảo trì."""

    class Meta:
        model = MaintenanceMode
        fields = ['is_enabled', 'message', 'allowed_ips']
        widgets = {
            'is_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'message': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Thông báo hiển thị khi bảo trì'
            }),
            'allowed_ips': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Mỗi IP trên 1 dòng'
            }),
        }
