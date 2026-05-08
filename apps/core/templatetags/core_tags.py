"""
Custom template tags cho core app.
"""
from django import template
from apps.core.utils import format_currency

register = template.Library()

register.filter('format_currency', format_currency)
