"""
Views cho app brands.
CRUD cho Brand model.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import models

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset
from .models import Brand
from .forms import BrandForm


@admin_required
def brand_list(request):
    """Trang danh sách thương hiệu."""
    brands = Brand.objects.all().order_by('name')

    search_query = request.GET.get('q', '')
    if search_query:
        brands = brands.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    status_filter = request.GET.get('status')
    if status_filter:
        is_active = status_filter == 'active'
        brands = brands.filter(is_active=is_active)

    page_obj, paginator = paginate_queryset(request, brands, 20)

    context = {
        'page_title': 'Quản lý thương hiệu',
        'active_menu': 'brands',
        'brands': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'brands/brand_list.html', context)


@admin_required
def brand_create(request):
    """Tạo thương hiệu mới."""
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tạo thương hiệu thành công!')
            return redirect('brands:brand_list')
    else:
        form = BrandForm()

    context = {
        'page_title': 'Thêm thương hiệu mới',
        'active_menu': 'brands',
        'form': form,
        'is_edit': False,
    }
    return render(request, 'brands/brand_form.html', context)


@admin_required
def brand_update(request, pk):
    """Cập nhật thương hiệu."""
    brand = get_object_or_404(Brand, pk=pk)

    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cập nhật thương hiệu "{brand.name}" thành công!')
            return redirect('brands:brand_list')
    else:
        form = BrandForm(instance=brand)

    context = {
        'page_title': f'Sửa thương hiệu',
        'active_menu': 'brands',
        'form': form,
        'brand': brand,
        'is_edit': True,
    }
    return render(request, 'brands/brand_form.html', context)


@admin_required
@require_http_methods(['POST'])
def brand_delete(request, pk):
    """Xóa thương hiệu."""
    brand = get_object_or_404(Brand, pk=pk)
    name = brand.name
    brand.delete()
    messages.success(request, f'Xóa thương hiệu "{name}" thành công!')
    return JsonResponse({'success': True, 'message': 'Xóa thành công!'})


@admin_required
@require_http_methods(['POST'])
def brand_toggle_status(request, pk):
    """Toggle trạng thái thương hiệu."""
    brand = get_object_or_404(Brand, pk=pk)
    brand.is_active = not brand.is_active
    brand.save()
    status_text = 'Kích hoạt' if brand.is_active else 'Vô hiệu hóa'
    return JsonResponse({
        'success': True,
        'message': f'{status_text} thương hiệu thành công!',
        'is_active': brand.is_active
    })
