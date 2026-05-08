"""
Views cho app inventory.
Quản lý tồn kho sản phẩm.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset
from apps.products.models import Product
from apps.categories.models import Category


@admin_required
def inventory_list(request):
    """Trang danh sách tồn kho."""
    products = Product.objects.select_related('category').all().order_by('-stock_quantity')

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category_id=category_filter)

    # Filter by stock status
    status_filter = request.GET.get('status')
    if status_filter == 'in_stock':
        products = products.filter(stock_quantity__gt=10)
    elif status_filter == 'low_stock':
        products = products.filter(stock_quantity__gt=0, stock_quantity__lte=10)
    elif status_filter == 'out_of_stock':
        products = products.filter(stock_quantity=0)

    # Paginate
    page_obj, paginator = paginate_queryset(request, products, 5)

    # Stats
    total_products = Product.objects.count()
    in_stock_count = Product.objects.filter(stock_quantity__gt=10).count()
    low_stock_count = Product.objects.filter(stock_quantity__gt=0, stock_quantity__lte=10).count()
    out_of_stock_count = Product.objects.filter(stock_quantity=0).count()

    # Categories for filter
    categories = Category.objects.filter(is_active=True).order_by('name')

    context = {
        'page_title': 'Quản lý tồn kho',
        'active_menu': 'inventory',
        'inventory': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'category_filter': category_filter,
        'status_filter': status_filter,
        'categories': categories,
        'total_products': total_products,
        'in_stock_count': in_stock_count,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
    }
    return render(request, 'inventory/inventory_list.html', context)


@admin_required
def inventory_adjustment(request):
    """Trang điều chỉnh tồn kho."""
    products = Product.objects.all().order_by('name')

    context = {
        'page_title': 'Điều chỉnh tồn kho',
        'active_menu': 'inventory',
        'products': products,
    }

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_change = request.POST.get('quantity_change')
        reason = request.POST.get('reason')
        notes = request.POST.get('notes', '')

        if not all([product_id, quantity_change, reason]):
            context['error'] = 'Vui lòng điền đầy đủ thông tin!'
            return render(request, 'inventory/inventory_adjustment.html', context)

        try:
            quantity_change = int(quantity_change)
        except ValueError:
            context['error'] = 'Số lượng thay đổi phải là số nguyên!'
            return render(request, 'inventory/inventory_adjustment.html', context)

        product = get_object_or_404(Product, pk=product_id)
        new_stock = product.stock_quantity + quantity_change

        if new_stock < 0:
            context['error'] = f'Số lượng không thể âm! Tồn kho hiện tại: {product.stock_quantity}'
            context['selected_product'] = product
            context['product_id'] = product_id
            context['quantity_change'] = quantity_change
            return render(request, 'inventory/inventory_adjustment.html', context)

        product.stock_quantity = new_stock
        product.save()

        context['success'] = f'Đã cập nhật tồn kho cho "{product.name}" từ {product.stock_quantity - quantity_change} → {new_stock}'
        context['selected_product'] = product
        context['new_stock'] = new_stock
        context['quantity_change'] = quantity_change

    return render(request, 'inventory/inventory_adjustment.html', context)
