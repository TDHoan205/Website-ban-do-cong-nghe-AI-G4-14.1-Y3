"""
Forms cho app inventory.
"""
from django import forms

from apps.categories.models import Category


class InventoryFilterForm(forms.Form):
    """Form lọc tồn kho."""

    STATUS_CHOICES = [
        ('', '-- Tất cả --'),
        ('in_stock', 'Còn hàng'),
        ('low_stock', 'Sắp hết hàng'),
        ('out_of_stock', 'Hết hàng'),
    ]

    status = forms.ChoiceField(
        label='Trạng thái tồn kho',
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.ModelChoiceField(
        label='Danh mục',
        queryset=Category.objects.filter(is_active=True).order_by('name'),
        required=False,
        empty_label='-- Tất cả --',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search = forms.CharField(
        label='Tìm kiếm',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tìm theo tên sản phẩm...'
        })
    )
