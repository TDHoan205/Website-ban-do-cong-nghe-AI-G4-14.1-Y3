"""
Forms cho app categories.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from crispy_forms.bootstrap import FormActions

from .models import Category


class CategoryForm(forms.ModelForm):
    """Form danh mục."""

    class Meta:
        model = Category
        fields = ['name', 'description', 'image_url', 'icon_name', 'display_order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên danh mục'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Mô tả danh mục'
            }),
            'image_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL hình ảnh'
            }),
            'icon_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên icon (VD: mobile-alt, laptop, headphones)'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Thứ tự hiển thị'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('icon_name', css_class='col-md-3'),
                Column('display_order', css_class='col-md-3'),
            ),
            'description',
            'image_url',
            'is_active',
            FormActions(
                Submit('submit', 'Lưu', css_class='btn-primary'),
                HTML('<a href="/categories/" class="btn btn-secondary">Hủy</a>')
            )
        )

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Category.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Danh mục này đã tồn tại!')
        return name
