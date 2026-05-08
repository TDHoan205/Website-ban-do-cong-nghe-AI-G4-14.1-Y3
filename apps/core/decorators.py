"""
Core decorators cho views.
Chứa các decorator dùng chung trong toàn bộ ứng dụng.
"""
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.http import JsonResponse
from functools import wraps


def admin_required(view_func):
    """
    Decorator yêu cầu quyền Admin hoặc Employee.
    Sử dụng: @admin_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Vui lòng đăng nhập!'
                }, status=401)
            return redirect('accounts:login')
        role = getattr(request.user, 'role', None)
        if role not in ['Admin', 'Employee'] and not request.user.is_staff:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Bạn không có quyền truy cập!'
                }, status=403)
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_only(view_func):
    """
    Decorator yêu cầu quyền Admin only.
    Sử dụng: @admin_only
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Vui lòng đăng nhập!'
                }, status=401)
            return redirect('accounts:login')
        role = getattr(request.user, 'role', None)
        if role != 'Admin' and not request.user.is_superuser:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Chỉ Admin mới có quyền truy cập!'
                }, status=403)
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def ajax_required(view_func):
    """
    Decorator yêu cầu request phải là AJAX.
    Sử dụng: @ajax_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Yêu cầu phải là AJAX!'
            }, status=400)
        return view_func(request, *args, **kwargs)
    return wrapper


def customer_required(view_func):
    """
    Decorator yêu cầu quyền Customer.
    Sử dụng: @customer_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Vui lòng đăng nhập!'
                }, status=401)
            return redirect('accounts:login')
        role = getattr(request.user, 'role', None)
        if role not in ['Customer', 'Admin', 'Employee']:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Bạn không có quyền truy cập!'
                }, status=403)
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def superuser_required(view_func):
    """
    Decorator yêu cầu Super User.
    Sử dụng: @superuser_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Vui lòng đăng nhập!'
                }, status=401)
            return redirect('accounts:login')
        if not request.user.is_superuser:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Chỉ Super User mới có quyền!'
                }, status=403)
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper
