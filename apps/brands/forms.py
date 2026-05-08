"""
Forms cho app brands.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML

from .models import Brand


class BrandForm(forms.ModelForm):
    """Form thương hiệu."""

    class Meta:
        model = Brand
        fields = ['name', 'description', 'logo_url', 'website', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên thương hiệu'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Mô tả thương hiệu'}),
            'logo_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL logo'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://brand.com'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-8'),
                Column('is_active', css_class='col-md-4 d-flex align-items-center'),
            ),
            'description',
            Row(
                Column('logo_url', css_class='col-md-6'),
                Column('website', css_class='col-md-6'),
            ),
            Submit('submit', 'Lưu', css_class='btn-primary'),
            HTML('<a href="/brands/" class="btn btn-secondary ms-2">Hủy</a>')
        )

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Brand.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Thương hiệu này đã tồn tại!')
        return name
