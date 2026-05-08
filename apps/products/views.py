"""
Views cho app products.
CRUD cho Product, ProductVariant, ProductImage models.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Q

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset, format_currency
from .models import Product, ProductVariant, ProductImage
from .forms import ProductForm, ProductVariantForm, ProductImageForm


@admin_required
def product_list(request):
    """Trang danh sách sản phẩm."""
    products = Product.objects.select_related('category', 'supplier').all().order_by('-created_at')

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category_id=category_filter)

    # Filter by supplier
    supplier_filter = request.GET.get('supplier')
    if supplier_filter:
        products = products.filter(supplier_id=supplier_filter)

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'available':
        products = products.filter(is_available=True, stock_quantity__gt=0)
    elif status_filter == 'out_of_stock':
        products = products.filter(stock_quantity=0)
    elif status_filter == 'hidden':
        products = products.filter(is_available=False)

    # Paginate
    page_obj, paginator = paginate_queryset(request, products, 5)

    # Get filter options
    from apps.categories.models import Category
    from apps.suppliers.models import Supplier
    categories = Category.objects.filter(is_active=True).order_by('name')
    suppliers = Supplier.objects.filter(is_active=True).order_by('name')

    context = {
        'page_title': 'Quản lý sản phẩm',
        'active_menu': 'products',
        'products': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'category_filter': category_filter,
        'supplier_filter': supplier_filter,
        'status_filter': status_filter,
        'categories': categories,
        'suppliers': suppliers,
    }
    return render(request, 'products/product_list.html', context)


@admin_required
def product_create(request):
    """Tạo sản phẩm mới."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Tạo sản phẩm "{product.name}" thành công!')
            return redirect('products:product_list')
    else:
        form = ProductForm()

    context = {
        'page_title': 'Thêm sản phẩm mới',
        'active_menu': 'products',
        'form': form,
        'is_edit': False,
    }
    return render(request, 'products/product_form.html', context)


@admin_required
def product_update(request, pk):
    """Cập nhật sản phẩm."""
    product = get_object_or_404(Product.objects.prefetch_related('variants', 'product_images'), pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cập nhật sản phẩm "{product.name}" thành công!')
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)

    context = {
        'page_title': 'Sửa sản phẩm',
        'active_menu': 'products',
        'form': form,
        'product': product,
        'is_edit': True,
    }
    return render(request, 'products/product_form.html', context)


@admin_required
@require_http_methods(['POST'])
def product_delete(request, pk):
    """Xóa sản phẩm."""
    product = get_object_or_404(Product, pk=pk)

    name = product.name
    product.delete()
    messages.success(request, f'Xóa sản phẩm "{name}" thành công!')

    return JsonResponse({'success': True, 'message': 'Xóa thành công!'})


@admin_required
@require_http_methods(['POST'])
def product_toggle_status(request, pk):
    """Toggle trạng thái sản phẩm."""
    product = get_object_or_404(Product, pk=pk)

    product.is_available = not product.is_available
    product.save()

    status_text = 'Hiển thị' if product.is_available else 'Ẩn'
    return JsonResponse({
        'success': True,
        'message': f'{status_text} sản phẩm thành công!',
        'is_available': product.is_available
    })


# =====================
# Product Variant Views
# =====================

@admin_required
def variant_list(request, product_pk):
    """Danh sách biến thể của sản phẩm."""
    product = get_object_or_404(Product, pk=product_pk)
    variants = product.variants.all().order_by('display_order')

    context = {
        'page_title': f'Biến thể - {product.name}',
        'active_menu': 'products',
        'product': product,
        'variants': variants,
    }
    return render(request, 'products/variant_list.html', context)


@admin_required
def variant_create(request, product_pk):
    """Tạo biến thể mới."""
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'POST':
        form = ProductVariantForm(request.POST)
        if form.is_valid():
            variant = form.save(commit=False)
            variant.product = product
            variant.save()
            messages.success(request, 'Tạo biến thể thành công!')
            return redirect('products:variant_list', product_pk=product_pk)
    else:
        form = ProductVariantForm()

    context = {
        'page_title': 'Thêm biến thể',
        'active_menu': 'products',
        'product': product,
        'form': form,
    }
    return render(request, 'products/variant_form.html', context)


@admin_required
def variant_update(request, product_pk, variant_pk):
    """Cập nhật biến thể."""
    product = get_object_or_404(Product, pk=product_pk)
    variant = get_object_or_404(ProductVariant, pk=variant_pk, product=product)

    if request.method == 'POST':
        form = ProductVariantForm(request.POST, instance=variant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật biến thể thành công!')
            return redirect('products:variant_list', product_pk=product_pk)
    else:
        form = ProductVariantForm(instance=variant)

    context = {
        'page_title': 'Sửa biến thể',
        'active_menu': 'products',
        'product': product,
        'variant': variant,
        'form': form,
    }
    return render(request, 'products/variant_form.html', context)


@admin_required
@require_http_methods(['POST'])
def variant_delete(request, product_pk, variant_pk):
    """Xóa biến thể."""
    variant = get_object_or_404(ProductVariant, pk=variant_pk, product_id=product_pk)
    variant.delete()
    messages.success(request, 'Xóa biến thể thành công!')
    return JsonResponse({'success': True})


# =====================
# Product Image Views
# =====================

@admin_required
def image_list(request, product_pk):
    """Danh sách hình ảnh của sản phẩm."""
    product = get_object_or_404(Product, pk=product_pk)
    images = product.product_images.all().order_by('display_order')

    context = {
        'page_title': f'Hình ảnh - {product.name}',
        'active_menu': 'products',
        'product': product,
        'images': images,
    }
    return render(request, 'products/image_list.html', context)


@admin_required
def image_create(request, product_pk):
    """Tạo hình ảnh mới."""
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'POST':
        form = ProductImageForm(request.POST)
        if form.is_valid():
            image = form.save(commit=False)
            image.product = product
            image.save()
            messages.success(request, 'Thêm hình ảnh thành công!')
            return redirect('products:image_list', product_pk=product_pk)
    else:
        form = ProductImageForm()

    context = {
        'page_title': 'Thêm hình ảnh',
        'active_menu': 'products',
        'product': product,
        'form': form,
    }
    return render(request, 'products/image_form.html', context)


@admin_required
@require_http_methods(['POST'])
def image_delete(request, product_pk, image_pk):
    """Xóa hình ảnh."""
    image = get_object_or_404(ProductImage, pk=image_pk, product_id=product_pk)
    image.delete()
    messages.success(request, 'Xóa hình ảnh thành công!')
    return JsonResponse({'success': True})


# =====================
# Bulk Actions
# =====================

@admin_required
def product_bulk(request):
    """Bulk actions cho sản phẩm (activate, hide, delete)."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'})

    import json
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        action = data.get('action')

        if not ids:
            return JsonResponse({'success': False, 'message': 'Không có sản phẩm nào được chọn'})

        products = Product.objects.filter(pk__in=ids)

        if action == 'activate':
            products.update(is_available=True)
            return JsonResponse({'success': True, 'message': f'Đã kích hoạt {len(ids)} sản phẩm'})
        elif action == 'hide':
            products.update(is_available=False)
            return JsonResponse({'success': True, 'message': f'Đã ẩn {len(ids)} sản phẩm'})
        elif action == 'delete':
            products.delete()
            return JsonResponse({'success': True, 'message': f'Đã xóa {len(ids)} sản phẩm'})
        else:
            return JsonResponse({'success': False, 'message': 'Hành động không hợp lệ'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Dữ liệu không hợp lệ'})
