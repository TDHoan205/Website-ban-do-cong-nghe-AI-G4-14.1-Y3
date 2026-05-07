"""
Core mixins for class-based views.
"""
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class AdminRequiredMixin:
    """
    Mixin to require admin or employee authentication for class-based views.
    Usage: class MyView(AdminRequiredMixin, ListView):
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth:login')
        if not (request.user.is_staff or request.user.role in ['Admin', 'Employee']):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AdminOnlyMixin:
    """
    Mixin to require admin-only authentication for class-based views.
    Usage: class MyView(AdminOnlyMixin, DeleteView):
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth:login')
        if request.user.role != 'Admin' and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CustomerRequiredMixin:
    """
    Mixin to require customer authentication.
    Usage: class MyView(CustomerRequiredMixin, View):
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth:login')
        if request.user.role not in ['Customer', 'Admin', 'Employee']:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
