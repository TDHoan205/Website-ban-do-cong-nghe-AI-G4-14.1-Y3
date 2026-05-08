"""
Forms cho app orders.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Fieldset
from crispy_forms.bootstrap import FormActions

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    """Form đơn hàng."""

    class Meta:
        model = Order
        fields = ['account', 'customer_name', 'customer_phone', 'customer_address', 'notes', 'status']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select'}),
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên khách hàng'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số điện thoại'
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Địa chỉ giao hàng'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ghi chú'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].required = False
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Thông tin khách hàng',
                Row(
                    Column('account', css_class='col-md-6'),
                    Column('customer_name', css_class='col-md-6'),
                ),
                Row(
                    Column('customer_phone', css_class='col-md-6'),
                    Column('customer_address', css_class='col-md-6'),
                ),
            ),
            'notes',
            Fieldset(
                'Trạng thái',
                'status',
            ),
            FormActions(
                Submit('submit', 'Lưu', css_class='btn-primary'),
                HTML('<a href="/orders/" class="btn btn-secondary">Hủy</a>')
            )
        )


class OrderItemForm(forms.ModelForm):
    """Form chi tiết đơn hàng."""

    class Meta:
        model = OrderItem
        fields = ['product', 'variant', 'product_name', 'variant_name', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'variant': forms.Select(attrs={'class': 'form-select'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'variant_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='col-md-6'),
                Column('variant', css_class='col-md-6'),
            ),
            'product_name',
            'variant_name',
            Row(
                Column('quantity', css_class='col-md-6'),
                Column('unit_price', css_class='col-md-6'),
            ),
            FormActions(
                Submit('submit', 'Lưu', css_class='btn-primary'),
            )
        )
