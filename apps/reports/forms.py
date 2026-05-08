"""
Forms cho app reports.
"""
from django import forms


class ReportFilterForm(forms.Form):
    """Form lọc báo cáo."""

    PERIOD_CHOICES = [
        ('', '-- Chọn --'),
        ('week', 'Tuần này'),
        ('month', 'Tháng này'),
        ('quarter', 'Quý này'),
        ('year', 'Năm này'),
        ('custom', 'Tùy chỉnh'),
    ]

    period = forms.ChoiceField(
        label='Khoảng thời gian',
        choices=PERIOD_CHOICES,
        initial='month',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        label='Từ ngày',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    date_to = forms.DateField(
        label='Đến ngày',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
