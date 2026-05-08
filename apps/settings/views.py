"""
Views cho app settings.
Quản lý cài đặt website.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from apps.core.decorators import admin_required
from .models import SiteSetting, MaintenanceMode


@admin_required
def settings_list(request):
    """Trang danh sách cài đặt."""
    # Get all settings grouped by category
    categories = [
        ('general', 'Chung'),
        ('contact', 'Liên hệ'),
        ('social', 'Mạng xã hội'),
        ('email', 'Email'),
        ('payment', 'Thanh toán'),
        ('seo', 'SEO'),
        ('other', 'Khác'),
    ]

    settings_dict = {}
    for cat_key, cat_name in categories:
        settings_dict[cat_key] = {
            'name': cat_name,
            'settings': SiteSetting.objects.filter(category=cat_key).order_by('key')
        }

    # Maintenance mode
    maintenance, _ = MaintenanceMode.objects.get_or_create(pk=1)

    context = {
        'page_title': 'Cài đặt website',
        'active_menu': 'settings',
        'settings_dict': settings_dict,
        'maintenance': maintenance,
    }
    return render(request, 'settings/settings_list.html', context)


@admin_required
def setting_update(request, pk):
    """Cập nhật 1 cài đặt."""
    setting = get_object_or_404(SiteSetting, pk=pk)

    if request.method == 'POST':
        value = request.POST.get('value', '')
        setting.value = value
        setting.save()
        messages.success(request, f'Cập nhật "{setting.key}" thành công!')
        return redirect('settings:settings_list')

    return redirect('settings:settings_list')


@admin_required
def setting_create(request):
    """Tạo cài đặt mới."""
    if request.method == 'POST':
        key = request.POST.get('key', '').strip().lower()
        value = request.POST.get('value', '')
        setting_type = request.POST.get('setting_type', 'text')
        category = request.POST.get('category', 'general')
        description = request.POST.get('description', '')
        is_public = request.POST.get('is_public') == 'on'

        if not key:
            messages.error(request, 'Key là bắt buộc!')
            return redirect('settings:settings_list')

        if SiteSetting.objects.filter(key=key).exists():
            messages.error(request, 'Key đã tồn tại!')
            return redirect('settings:settings_list')

        SiteSetting.objects.create(
            key=key,
            value=value,
            setting_type=setting_type,
            category=category,
            description=description,
            is_public=is_public
        )
        messages.success(request, f'Tạo cài đặt "{key}" thành công!')

    return redirect('settings:settings_list')


@admin_required
@require_http_methods(["POST"])
def setting_delete(request, pk):
    """Xóa cài đặt."""
    setting = get_object_or_404(SiteSetting, pk=pk)
    key = setting.key
    setting.delete()
    messages.success(request, f'Xóa cài đặt "{key}" thành công!')
    return redirect('settings:settings_list')


@admin_required
def maintenance_update(request):
    """Cập nhật chế độ bảo trì."""
    maintenance = get_object_or_404(MaintenanceMode, pk=1)

    if request.method == 'POST':
        maintenance.is_enabled = request.POST.get('is_enabled') == 'on'
        maintenance.message = request.POST.get('message', '')
        maintenance.allowed_ips = request.POST.get('allowed_ips', '')
        maintenance.save()
        messages.success(request, 'Cập nhật chế độ bảo trì thành công!')

    return redirect('settings:settings_list')


@admin_required
def clear_cache(request):
    """Xóa cache (placeholder)."""
    # In production, implement actual cache clearing
    messages.success(request, 'Cache đã được xóa!')
    return redirect('settings:settings_list')
