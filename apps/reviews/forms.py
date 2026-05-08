"""
Forms cho app reviews.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML

from .models import Review


class ReviewForm(forms.ModelForm):
    """Form đánh giá (read-only cho admin)."""

    class Meta:
        model = Review
        fields = ['product', 'account', 'rating', 'title', 'comment', 'is_approved']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'account': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.Select(attrs={'class': 'form-select'}, choices=[(i, f'{i} ★') for i in range(1, 6)]),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề đánh giá'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Nội dung bình luận'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='col-md-6'),
                Column('account', css_class='col-md-6'),
            ),
            Row(
                Column('rating', css_class='col-md-4'),
                Column('is_approved', css_class='col-md-4 d-flex align-items-center'),
            ),
            'title',
            'comment',
            Submit('submit', 'Lưu', css_class='btn-primary'),
            HTML('<a href="/reviews/" class="btn btn-secondary ms-2">Hủy</a>')
        )
