"""
Forms cho app cart.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .models import CartItem


class AddToCartForm(forms.Form):
    """Form thêm sản phẩm vào giỏ hàng."""
    quantity = forms.IntegerField(
        label='Số lượng',
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1
        })
    )

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields['quantity'].widget.attrs['max'] = product.stock_quantity


class CartItemForm(forms.ModelForm):
    """Form giỏ hàng."""

    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'quantity',
            Submit('submit', 'Cập nhật', css_class='btn-primary btn-sm mt-2')
        )
