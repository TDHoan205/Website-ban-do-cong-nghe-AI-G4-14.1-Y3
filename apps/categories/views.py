"""
Views cho app categories.
CRUD cho Category model.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import models

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset
from .models import Category
from .forms import CategoryForm


@admin_required
def category_list(request):
    """Trang danh sách danh mục."""
    categories = Category.objects.all().order_by('display_order', 'name')

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        categories = categories.filter(name__icontains=search_query)

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        is_active = status_filter == 'active'
        categories = categories.filter(is_active=is_active)

    # Paginate
    page_obj, paginator = paginate_queryset(request, categories, 5)

    context = {
        'page_title': 'Quản lý danh mục',
        'active_menu': 'categories',
        'categories': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'categories/category_list.html', context)


@admin_required
def category_create(request):
    """Tạo danh mục mới."""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tạo danh mục thành công!')
            return redirect('categories:category_list')
    else:
        form = CategoryForm()

    context = {
        'page_title': 'Thêm danh mục mới',
        'active_menu': 'categories',
        'form': form,
        'is_edit': False,
    }
    return render(request, 'categories/category_form.html', context)


@admin_required
def category_update(request, pk):
    """Cập nhật danh mục."""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật danh mục thành công!')
            return redirect('categories:category_list')
    else:
        form = CategoryForm(instance=category)

    context = {
        'page_title': 'Sửa danh mục',
        'active_menu': 'categories',
        'form': form,
        'category': category,
        'is_edit': True,
    }
    return render(request, 'categories/category_form.html', context)


@admin_required
@require_http_methods(['POST'])
def category_delete(request, pk):
    """Xóa danh mục."""
    category = get_object_or_404(Category, pk=pk)

    if category.products.exists():
        return JsonResponse({
            'success': False,
            'message': 'Không thể xóa! Danh mục đang có sản phẩm.'
        })

    name = category.name
    category.delete()
    messages.success(request, f'Xóa danh mục "{name}" thành công!')

    return JsonResponse({'success': True, 'message': 'Xóa thành công!'})


@admin_required
@require_http_methods(['POST'])
def category_toggle_status(request, pk):
    """Toggle trạng thái danh mục."""
    category = get_object_or_404(Category, pk=pk)

    category.is_active = not category.is_active
    category.save()

    status_text = 'Kích hoạt' if category.is_active else 'Vô hiệu hóa'
    return JsonResponse({
        'success': True,
        'message': f'{status_text} danh mục thành công!',
        'is_active': category.is_active
    })
