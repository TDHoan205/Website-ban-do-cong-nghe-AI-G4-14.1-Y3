"""
Core utilities: decorators, mixins, and helper functions.
"""
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps


def admin_required(view_func):
    """
    Decorator to require admin or employee authentication.
    Usage: @admin_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth:login')
        if not (request.user.is_staff or request.user.role in ['Admin', 'Employee']):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_only(view_func):
    """
    Decorator to require admin-only authentication.
    Usage: @admin_only
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth:login')
        if request.user.role != 'Admin' and not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def ajax_required(view_func):
    """
    Decorator to require AJAX request.
    Usage: @ajax_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest('AJAX required')
        return view_func(request, *args, **kwargs)
    return wrapper
