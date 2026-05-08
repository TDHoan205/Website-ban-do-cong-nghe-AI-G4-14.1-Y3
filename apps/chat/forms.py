"""
Forms cho app chat.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import ChatMessage


class ChatMessageForm(forms.ModelForm):
    """Form gửi tin nhắn chat."""

    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Nhập tin nhắn...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'message',
            Submit('submit', 'Gửi', css_class='btn-primary mt-2')
        )
