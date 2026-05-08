"""
Views cho app suppliers.
CRUD cho Supplier model.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import models

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset
from .models import Supplier
from .forms import SupplierForm


@admin_required
def supplier_list(request):
    """Trang danh sách nhà cung cấp."""
    suppliers = Supplier.objects.all().order_by('name')

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        suppliers = suppliers.filter(
            models.Q(name__icontains=search_query) |
            models.Q(contact_person__icontains=search_query) |
            models.Q(phone__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        is_active = status_filter == 'active'
        suppliers = suppliers.filter(is_active=is_active)

    # Paginate
    page_obj, paginator = paginate_queryset(request, suppliers, 5)

    context = {
        'page_title': 'Quản lý nhà cung cấp',
        'active_menu': 'suppliers',
        'suppliers': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'suppliers/supplier_list.html', context)


@admin_required
def supplier_create(request):
    """Tạo nhà cung cấp mới."""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tạo nhà cung cấp thành công!')
            return redirect('suppliers:supplier_list')
    else:
        form = SupplierForm()

    context = {
        'page_title': 'Thêm nhà cung cấp mới',
        'active_menu': 'suppliers',
        'form': form,
        'is_edit': False,
    }
    return render(request, 'suppliers/supplier_form.html', context)


@admin_required
def supplier_update(request, pk):
    """Cập nhật nhà cung cấp."""
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật nhà cung cấp thành công!')
            return redirect('suppliers:supplier_list')
    else:
        form = SupplierForm(instance=supplier)

    context = {
        'page_title': 'Sửa nhà cung cấp',
        'active_menu': 'suppliers',
        'form': form,
        'supplier': supplier,
        'is_edit': True,
    }
    return render(request, 'suppliers/supplier_form.html', context)


@admin_required
@require_http_methods(['POST'])
def supplier_delete(request, pk):
    """Xóa nhà cung cấp."""
    supplier = get_object_or_404(Supplier, pk=pk)

    if supplier.products.exists():
        return JsonResponse({
            'success': False,
            'message': 'Không thể xóa! Nhà cung cấp đang có sản phẩm.'
        })

    name = supplier.name
    supplier.delete()
    messages.success(request, f'Xóa nhà cung cấp "{name}" thành công!')

    return JsonResponse({'success': True, 'message': 'Xóa thành công!'})


@admin_required
@require_http_methods(['POST'])
def supplier_toggle_status(request, pk):
    """Toggle trạng thái nhà cung cấp."""
    supplier = get_object_or_404(Supplier, pk=pk)

    supplier.is_active = not supplier.is_active
    supplier.save()

    status_text = 'Kích hoạt' if supplier.is_active else 'Vô hiệu hóa'
    return JsonResponse({
        'success': True,
        'message': f'{status_text} nhà cung cấp thành công!',
        'is_active': supplier.is_active
    })
