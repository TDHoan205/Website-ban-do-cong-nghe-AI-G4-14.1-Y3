"""
Forms cho app suppliers.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from crispy_forms.bootstrap import FormActions

from .models import Supplier


class SupplierForm(forms.ModelForm):
    """Form nhà cung cấp."""

    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'address', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên nhà cung cấp'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Người liên hệ'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số điện thoại (VD: 0909 123 456)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@company.com'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Địa chỉ'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            Row(
                Column('contact_person', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6 d-flex align-items-center'),
            ),
            'address',
            FormActions(
                Submit('submit', 'Lưu', css_class='btn-primary'),
                HTML('<a href="/suppliers/" class="btn btn-secondary">Hủy</a>')
            )
        )
