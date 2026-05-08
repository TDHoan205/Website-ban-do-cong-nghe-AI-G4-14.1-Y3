"""
Forms cho app dashboard.
"""
from django import forms


class ReportPeriodForm(forms.Form):
    """Form chọn khoảng thời gian báo cáo."""

    PERIOD_CHOICES = [
        ('', '-- Chọn --'),
        ('7days', '7 ngày qua'),
        ('30days', '30 ngày qua'),
        ('this_month', 'Tháng này'),
        ('this_year', 'Năm nay'),
    ]

    period = forms.ChoiceField(
        label='Khoảng thời gian',
        choices=PERIOD_CHOICES,
        initial='30days',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
