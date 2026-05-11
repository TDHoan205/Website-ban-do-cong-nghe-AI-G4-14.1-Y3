"""
Views cho app inventory.
Quan ly ton kho san pham va bien dong kho.
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
from .models import Inventory, InventoryMovement


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
    """Trang dieu chinh ton kho + ghi nhan bien dong kho."""
    products = Product.objects.all().order_by('name')

    context = {
        'page_title': 'Dieu chinh ton kho',
        'active_menu': 'inventory',
        'products': products,
    }

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_change = request.POST.get('quantity_change')
        reason = request.POST.get('reason')
        notes = request.POST.get('notes', '')

        if not all([product_id, quantity_change, reason]):
            context['error'] = 'Vui long dien day du thong tin!'
            return render(request, 'inventory/inventory_adjustment.html', context)

        try:
            quantity_change = int(quantity_change)
        except ValueError:
            context['error'] = 'So luong thay doi phai la so nguyen!'
            return render(request, 'inventory/inventory_adjustment.html', context)

        product = get_object_or_404(Product, pk=product_id)
        new_stock = product.stock_quantity + quantity_change

        if new_stock < 0:
            context['error'] = f'So luong khong the am! Ton kho hien tai: {product.stock_quantity}'
            context['selected_product'] = product
            context['product_id'] = product_id
            context['quantity_change'] = quantity_change
            return render(request, 'inventory/inventory_adjustment.html', context)

        # Xac dinh loai bien dong
        if quantity_change > 0:
            movement_type = 'IN'
        elif quantity_change < 0:
            movement_type = 'OUT'
        else:
            movement_type = 'ADJUST'

        # Ghi nhan bien dong kho
        InventoryMovement.objects.create(
            product=product,
            movement_type=movement_type,
            quantity=abs(quantity_change),
            reason=reason,
            notes=notes,
            created_by=request.user,
        )

        # Cap nhat ton kho
        product.stock_quantity = new_stock
        product.save()

        context['success'] = f'Da cap nhat ton kho cho "{product.name}" tu {product.stock_quantity - quantity_change} -> {new_stock}'
        context['selected_product'] = product
        context['new_stock'] = new_stock
        context['quantity_change'] = quantity_change

    return render(request, 'inventory/inventory_adjustment.html', context)


@admin_required
def inventory_movements(request):
    """Trang lich su bien dong kho."""
    movements = InventoryMovement.objects.select_related(
        'product', 'created_by', 'related_order'
    ).all().order_by('-created_at')

    product_filter = request.GET.get('product')
    if product_filter:
        movements = movements.filter(product_id=product_filter)

    movement_type_filter = request.GET.get('type')
    if movement_type_filter:
        movements = movements.filter(movement_type=movement_type_filter)

    search_query = request.GET.get('q', '')
    if search_query:
        movements = movements.filter(
            Q(product__name__icontains=search_query) |
            Q(reason__icontains=search_query)
        )

    page_obj, paginator = paginate_queryset(request, movements, 20)

    products = Product.objects.order_by('name')

    context = {
        'page_title': 'Lich su bien dong kho',
        'active_menu': 'inventory',
        'movements': page_obj,
        'paginator': paginator,
        'products': products,
        'product_filter': product_filter,
        'type_filter': movement_type_filter,
        'search_query': search_query,
        'movement_types': InventoryMovement.MOVEMENT_TYPES,
    }
    return render(request, 'inventory/inventory_movements.html', context)


@admin_required
@require_http_methods(["GET"])
def low_stock_alerts(request):
    """API lay danh sach san pham ton kho thap."""
    threshold = int(request.GET.get('threshold', 10))
    products = Product.objects.filter(
        stock_quantity__lte=threshold,
        is_available=True
    ).select_related('category').order_by('stock_quantity')[:50]

    items = [
        {
            'product_id': p.product_id,
            'name': p.name,
            'category': p.category.name if p.category else '',
            'stock': p.stock_quantity,
            'threshold': threshold,
        }
        for p in products
    ]

    return JsonResponse({
        'success': True,
        'items': items,
        'total': len(items)
    })
