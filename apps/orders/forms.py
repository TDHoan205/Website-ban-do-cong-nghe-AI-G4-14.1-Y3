"""
Forms cho app orders.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Fieldset
from crispy_forms.bootstrap import FormActions

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    """Form don hang."""

    class Meta:
        model = Order
        fields = [
            'account', 'customer_name', 'customer_phone', 'customer_address',
            'notes', 'status', 'payment_method', 'payment_status',
            'shipping_method', 'tracking_number', 'admin_notes',
        ]
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select'}),
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ten khach hang'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'So dien thoai'
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dia chi giao hang'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ghi chu'
            }),
            'admin_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ghi chu noi bo (chi admin nhin thay)'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'shipping_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phuong thuc van chuyen'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ma van don'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].required = False
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Thong tin khach hang',
                Row(
                    Column('account', css_class='col-md-4'),
                    Column('customer_name', css_class='col-md-4'),
                    Column('customer_phone', css_class='col-md-4'),
                ),
                'customer_address',
            ),
            Fieldset(
                'Thong tin thanh toan',
                Row(
                    Column('payment_method', css_class='col-md-4'),
                    Column('payment_status', css_class='col-md-4'),
                    Column('status', css_class='col-md-4'),
                ),
            ),
            Fieldset(
                'Van chuyen',
                Row(
                    Column('shipping_method', css_class='col-md-6'),
                    Column('tracking_number', css_class='col-md-6'),
                ),
            ),
            'notes',
            'admin_notes',
            FormActions(
                Submit('submit', 'Luu', css_class='btn-primary'),
                HTML('<a href="/orders/" class="btn btn-secondary">Huy</a>')
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
