"""
Forms cho app faqs.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from crispy_forms.bootstrap import FormActions

from .models import FAQ


class FAQForm(forms.ModelForm):
    """Form FAQ."""

    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category', 'keywords', 'priority', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập câu hỏi'
            }),
            'answer': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Nhập câu trả lời'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'keywords': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Từ khóa liên quan, cách nhau bởi dấu phẩy'
            }),
            'priority': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Độ ưu tiên (số càng lớn càng ưu tiên)'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'question',
            'answer',
            Row(
                Column('category', css_class='col-md-6'),
                Column('priority', css_class='col-md-6'),
            ),
            'keywords',
            'is_active',
            FormActions(
                Submit('submit', 'Lưu', css_class='btn-primary'),
                HTML('<a href="/faqs/" class="btn btn-secondary">Hủy</a>')
            )
        )
