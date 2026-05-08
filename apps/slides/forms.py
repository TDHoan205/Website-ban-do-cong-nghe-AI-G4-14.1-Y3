"""
Forms cho app slides.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML

from .models import Slide


class SlideForm(forms.ModelForm):
    """Form slide banner."""

    class Meta:
        model = Slide
        fields = ['title', 'subtitle', 'image_url', 'link', 'button_text', 'display_order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề slide'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phụ đề'}),
            'image_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL hình ảnh slide'}),
            'link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link khi click (VD: /products/)'}),
            'button_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Text nút bấm (VD: Xem ngay)'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-8'),
                Column('display_order', css_class='col-md-2'),
                Column('is_active', css_class='col-md-2 d-flex align-items-center'),
            ),
            'subtitle',
            Row(
                Column('image_url', css_class='col-md-8'),
                Column('button_text', css_class='col-md-4'),
            ),
            'link',
            Submit('submit', 'Lưu', css_class='btn-primary'),
            HTML('<a href="/slides/" class="btn btn-secondary ms-2">Hủy</a>')
        )
