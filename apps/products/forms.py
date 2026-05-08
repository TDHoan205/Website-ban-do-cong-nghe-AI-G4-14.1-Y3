"""
Forms cho app products.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Fieldset
from crispy_forms.bootstrap import FormActions, Accordion, AccordionGroup

from .models import Product, ProductVariant, ProductImage
from apps.categories.models import Category
from apps.suppliers.models import Supplier


class ProductForm(forms.ModelForm):
    """Form sản phẩm."""

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'image_url', 'price', 'original_price',
            'stock_quantity', 'is_available', 'is_new', 'is_hot',
            'discount_percent', 'specifications', 'category', 'supplier'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên sản phẩm'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Mô tả sản phẩm'
            }),
            'image_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL hình ảnh'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Giá bán'
            }),
            'original_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Giá gốc'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số lượng tồn'
            }),
            'discount_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phần trăm giảm giá (0-100)'
            }),
            'specifications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Thông số kỹ thuật (JSON)'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_new': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_hot': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True).order_by('name')
        self.fields['supplier'].queryset = Supplier.objects.filter(is_active=True).order_by('name')
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Fieldset(
                'Thông tin cơ bản',
                Row(
                    Column('name', css_class='col-md-8'),
                    Column('category', css_class='col-md-4'),
                ),
                'description',
            ),
            Fieldset(
                'Giá cả',
                Row(
                    Column('price', css_class='col-md-4'),
                    Column('original_price', css_class='col-md-4'),
                    Column('discount_percent', css_class='col-md-4'),
                ),
            ),
            Fieldset(
                'Hình ảnh',
                'image_url',
            ),
            Fieldset(
                'Kho hàng',
                Row(
                    Column('stock_quantity', css_class='col-md-4'),
                    Column('supplier', css_class='col-md-4'),
                    Column('is_available', css_class='col-md-4 d-flex align-items-center'),
                ),
                Row(
                    Column('is_new', css_class='col-md-4'),
                    Column('is_hot', css_class='col-md-4'),
                ),
            ),
            'specifications',
            FormActions(
                Submit('submit', 'Lưu', css_class='btn-primary'),
                HTML('<a href="/products/" class="btn btn-secondary">Hủy</a>')
            )
        )

    def clean_price(self):
        price = self.cleaned_data['price']
        if price and price < 0:
            raise forms.ValidationError('Giá không được âm!')
        return price


class ProductVariantForm(forms.ModelForm):
    """Form biến thể sản phẩm."""

    class Meta:
        model = ProductVariant
        fields = ['color', 'storage', 'ram', 'variant_name', 'sku', 
                  'price', 'original_price', 'stock_quantity', 'display_order', 'is_active']
        widgets = {
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Màu sắc (VD: Đen, Trắng, Xanh)'
            }),
            'storage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dung lượng (VD: 128GB, 256GB)'
            }),
            'ram': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RAM (VD: 8GB, 12GB)'
            }),
            'variant_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên biến thể'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mã SKU'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Giá'
            }),
            'original_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Giá gốc'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số lượng tồn'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Thứ tự'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('color', css_class='col-md-4'),
                Column('storage', css_class='col-md-4'),
                Column('ram', css_class='col-md-4'),
            ),
            'variant_name',
            'sku',
            Row(
                Column('price', css_class='col-md-4'),
                Column('original_price', css_class='col-md-4'),
                Column('stock_quantity', css_class='col-md-4'),
            ),
            Row(
                Column('display_order', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6 d-flex align-items-center'),
            ),
            FormActions(
                Submit('submit', 'Lưu', css_class='btn-primary'),
            )
        )


class ProductImageForm(forms.ModelForm):
    """Form hình ảnh sản phẩm."""

    class Meta:
        model = ProductImage
        fields = ['image_url', 'display_order', 'is_primary']
        widgets = {
            'image_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL hình ảnh'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Thứ tự hiển thị'
            }),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'image_url',
            Row(
                Column('display_order', css_class='col-md-6'),
                Column('is_primary', css_class='col-md-6 d-flex align-items-center'),
            ),
            FormActions(
                Submit('submit', 'Lưu', css_class='btn-primary'),
            )
        )
