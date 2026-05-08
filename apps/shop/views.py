"""
Views cho app shop.
Frontend - Trang chủ, danh sách sản phẩm, chi tiết, giỏ hàng.
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.db import transaction
from django.utils import timezone
from decimal import Decimal

from apps.products.models import Product, ProductVariant, ProductImage
from apps.categories.models import Category
from apps.cart.models import CartItem
from apps.cart.forms import AddToCartForm
from apps.orders.models import Order, OrderItem
from apps.core.utils import generate_order_code


def shop_home(request):
    """Trang chủ shop - hiển thị hero banner, danh mục, sản phẩm."""
    # Danh mục active
    categories = Category.objects.filter(is_active=True).order_by('display_order', 'name')[:8]
    
    # Số sản phẩm mỗi trang
    per_page = 4
    
    # Sản phẩm mới - có phân trang
    new_products_qs = Product.objects.filter(
        is_available=True,
        is_new=True
    ).select_related('category').order_by('-created_at')
    
    new_page = request.GET.get('new_page', 1)
    new_paginator = Paginator(new_products_qs, per_page)
    try:
        new_products = new_paginator.page(new_page)
    except (PageNotAnInteger, EmptyPage):
        new_products = new_paginator.page(1)
    
    # Sản phẩm hot - có phân trang
    hot_products_qs = Product.objects.filter(
        is_available=True,
        is_hot=True
    ).select_related('category').order_by('-rating', '-created_at')
    
    hot_page = request.GET.get('hot_page', 1)
    hot_paginator = Paginator(hot_products_qs, per_page)
    try:
        hot_products = hot_paginator.page(hot_page)
    except (PageNotAnInteger, EmptyPage):
        hot_products = hot_paginator.page(1)
    
    # Sản phẩm deal (đang giảm giá)
    deal_products = Product.objects.filter(
        is_available=True
    ).exclude(
        original_price__isnull=True
    ).exclude(
        original_price=0
    ).filter(
        original_price__gt=models.F('price')
    ).select_related('category').order_by('-discount_percent')[:3]
    
    # Sản phẩm nổi bật
    featured_products = Product.objects.filter(
        is_available=True
    ).select_related('category').order_by('-rating', '-created_at')[:8]
    
    context = {
        'categories': categories,
        'new_products': new_products,
        'hot_products': hot_products,
        'deal_products': deal_products,
        'featured_products': featured_products,
        'new_paginator': new_paginator,
        'hot_paginator': hot_paginator,
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    """Trang danh sách sản phẩm với bộ lọc và phân trang."""
    products = Product.objects.filter(is_available=True).select_related('category')
    
    # Lọc theo từ khóa tìm kiếm
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Lọc theo danh mục
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Lọc theo filter (new, hot)
    filter_type = request.GET.get('filter')
    if filter_type == 'new':
        products = products.filter(is_new=True)
    elif filter_type == 'hot':
        products = products.filter(is_hot=True)
    
    # Sắp xếp
    sort_by = request.GET.get('sort', '-created_at')
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        'rating': '-rating',
        'newest': '-created_at',
        '-created_at': '-created_at',
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    # Lọc theo khoảng giá
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Phân trang
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    # Lấy danh sách danh mục cho filter sidebar
    categories = Category.objects.filter(is_active=True).order_by('name')
    
    context = {
        'products': products_page,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
        'filter_type': filter_type,
        'sort_by': sort_by,
        'min_price': min_price or '',
        'max_price': max_price or '',
    }
    return render(request, 'shop/products.html', context)


def product_detail(request, product_id):
    """Trang chi tiết sản phẩm."""
    product = get_object_or_404(
        Product.objects.select_related('category', 'supplier').prefetch_related(
            'variants', 'product_images'
        ),
        product_id=product_id
    )
    
    # Lấy các biến thể active
    variants_qs = product.variants.filter(is_active=True).order_by('display_order', 'variant_name')
    
    # Lấy hình ảnh sản phẩm
    images_qs = product.product_images.all()
    
    # Prepare images_by_variant cho JS gallery (tương tự C# ProductDetailDto)
    images_by_variant = {}
    all_images = []
    
    for img in images_qs:
        img_data = {
            'image_id': img.image_id,
            'image_url': img.image_url,
            'variant_id': img.variant_id,
            'is_primary': img.is_primary,
            'is_thumbnail': img.is_thumbnail,
            'display_order': img.display_order,
            'alt_text': img.alt_text or '',
        }
        
        if img.variant_id:
            key = f"variant_{img.variant_id}"
        else:
            key = "default"
        
        if key not in images_by_variant:
            images_by_variant[key] = []
        images_by_variant[key].append(img_data)
        all_images.append(img_data)
    
    # Variant list cho JS (tương tự C# ProductService)
    variants_list = []
    for v in variants_qs:
        config = ''
        if v.storage:
            config = v.storage
        if v.ram:
            config = config + (' / ' if config else '') + v.ram
        
        variants_list.append({
            'variant_id': v.variant_id,
            'color': v.color or '',
            'storage': v.storage or '',
            'ram': v.ram or '',
            'config': config,
            'price': float(v.price) if v.price else float(product.price),
            'original_price': float(v.original_price) if v.original_price else None,
            'stock_quantity': v.stock_quantity,
        })
    
    # Product JSON cho JS
    product_json = {
        'product_id': product.product_id,
        'name': product.name,
        'price': float(product.price),
        'original_price': float(product.original_price) if product.original_price else None,
        'discount_percent': product.discount_percent,
        'stock_quantity': product.stock_quantity,
        'category_name': product.category.name if product.category else '',
        'supplier_name': product.supplier.name if product.supplier else '',
        'image_url': product.image_url or '',
    }
    
    # Sản phẩm liên quan (cùng danh mục)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(product_id=product_id).order_by('-rating')[:4]
    
    # Form thêm vào giỏ hàng
    add_to_cart_form = AddToCartForm(product=product)
    
    # Lấy giỏ hàng hiện tại (nếu đã đăng nhập)
    cart_items_count = 0
    if request.user.is_authenticated:
        cart_items_count = CartItem.objects.filter(account=request.user).count()
    
    # Unique colors và configs cho UI
    unique_colors = list(set(v.get('color', '') for v in variants_list if v.get('color')))[:10]
    unique_configs = []
    seen_configs = set()
    for v in variants_list:
        cfg = v.get('config', '')
        if cfg and cfg not in seen_configs:
            seen_configs.add(cfg)
            unique_configs.append({
                'key': cfg,
                'storage': v.get('storage', ''),
                'ram': v.get('ram', ''),
            })
    
    context = {
        'product': product,
        'variants': variants_list,
        'all_images': all_images,
        'images_by_variant': images_by_variant,
        'product_json': json.dumps(product_json),
        'variants_json': json.dumps(variants_list),
        'images_by_variant_json': json.dumps(images_by_variant),
        'unique_colors': unique_colors,
        'unique_configs': unique_configs,
        'related_products': related_products,
        'add_to_cart_form': add_to_cart_form,
        'cart_items_count': cart_items_count,
    }
    return render(request, 'shop/product_detail.html', context)


def cart_view(request):
    """Trang giỏ hàng."""
    if not request.user.is_authenticated:
        messages.warning(request, 'Vui lòng đăng nhập để xem giỏ hàng.')
        return redirect('accounts:login')
    
    cart_items = CartItem.objects.filter(
        account=request.user
    ).select_related('product', 'variant')
    
    # Tính tổng tiền
    total = sum(item.subtotal for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'total_items': total_items,
    }
    return render(request, 'shop/cart.html', context)


def checkout_view(request):
    """Trang thanh toán."""
    if not request.user.is_authenticated:
        messages.warning(request, 'Vui lòng đăng nhập để thanh toán.')
        return redirect('accounts:login')

    cart_items = CartItem.objects.filter(
        account=request.user
    ).select_related('product', 'variant')

    if not cart_items.exists():
        messages.warning(request, 'Giỏ hàng trống!')
        return redirect('shop:cart')

    total = sum(item.subtotal for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '')
        customer_phone = request.POST.get('customer_phone', '')
        customer_address = request.POST.get('customer_address', '')
        notes = request.POST.get('notes', '')

        if not customer_name or not customer_phone or not customer_address:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin giao hàng!')
        else:
            with transaction.atomic():
                order = Order.objects.create(
                    account=request.user,
                    order_code=generate_order_code(),
                    total_amount=total,
                    status='Pending',
                    customer_name=customer_name,
                    customer_phone=customer_phone,
                    customer_address=customer_address,
                    notes=notes,
                )

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        variant=item.variant,
                        product_name=item.product.name,
                        variant_name=item.variant.variant_name if item.variant else '',
                        quantity=item.quantity,
                        unit_price=item.unit_price,
                        subtotal=item.subtotal,
                    )

                    if item.variant:
                        item.variant.stock_quantity = max(0, item.variant.stock_quantity - item.quantity)
                        item.variant.save()
                    else:
                        item.product.stock_quantity = max(0, item.product.stock_quantity - item.quantity)
                        item.product.save()

                cart_items.delete()

                messages.success(request, f'Đặt hàng thành công! Mã đơn hàng: {order.order_code}')
                return redirect('orders:order_detail', pk=order.pk)

    context = {
        'cart_items': cart_items,
        'total': total,
        'total_items': total_items,
        'user': request.user,
    }
    return render(request, 'shop/checkout.html', context)


def add_to_cart(request):
    """API thêm sản phẩm vào giỏ hàng."""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.',
            'requires_login': True
        })
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        variant_id = request.POST.get('variant_id')
        
        try:
            product = Product.objects.get(product_id=product_id, is_available=True)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sản phẩm không tồn tại.'})
        
        variant = None
        if variant_id:
            try:
                variant = ProductVariant.objects.get(variant_id=variant_id, is_active=True)
            except ProductVariant.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Biến thể không tồn tại.'})
        
        # Kiểm tra tồn kho
        if variant:
            stock = variant.stock_quantity
        else:
            stock = product.stock_quantity
        
        if quantity > stock:
            return JsonResponse({
                'success': False, 
                'message': f'Sản phẩm chỉ còn {stock} trong kho.'
            })
        
        # Thêm hoặc cập nhật giỏ hàng
        cart_item, created = CartItem.objects.get_or_create(
            account=request.user,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > stock:
                cart_item.quantity = stock
            cart_item.save()
        
        # Đếm số lượng trong giỏ
        cart_count = CartItem.objects.filter(account=request.user).count()
        
        return JsonResponse({
            'success': True,
            'message': 'Đã thêm sản phẩm vào giỏ hàng!',
            'cart_count': cart_count,
            'quantity': cart_item.quantity
        })
    
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ.'})


def update_cart(request):
    """API cập nhật số lượng sản phẩm trong giỏ hàng."""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Vui lòng đăng nhập.'})
    
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            cart_item = CartItem.objects.get(cart_item_id=cart_item_id, account=request.user)
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sản phẩm không có trong giỏ hàng.'})
        
        if quantity <= 0:
            cart_item.delete()
            return JsonResponse({
                'success': True,
                'message': 'Đã xóa sản phẩm khỏi giỏ hàng.',
                'deleted': True
            })
        
        # Kiểm tra tồn kho
        stock = cart_item.variant.stock_quantity if cart_item.variant_id else cart_item.product.stock_quantity
        if quantity > stock:
            return JsonResponse({
                'success': False,
                'message': f'Chỉ còn {stock} sản phẩm trong kho.',
                'quantity': cart_item.quantity
            })
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Đã cập nhật số lượng.',
            'quantity': quantity,
            'subtotal': str(cart_item.subtotal)
        })
    
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ.'})


def remove_from_cart(request):
    """API xóa sản phẩm khỏi giỏ hàng."""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Vui lòng đăng nhập.'})
    
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        
        try:
            cart_item = CartItem.objects.get(cart_item_id=cart_item_id, account=request.user)
            cart_item.delete()
            
            # Tính lại tổng
            remaining_items = CartItem.objects.filter(account=request.user)
            total = sum(item.subtotal for item in remaining_items)
            
            return JsonResponse({
                'success': True,
                'message': 'Đã xóa sản phẩm khỏi giỏ hàng.',
                'cart_count': remaining_items.count(),
                'total': str(total)
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sản phẩm không có trong giỏ hàng.'})
    
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ.'})


def get_cart_count(request):
    """API lấy số lượng sản phẩm trong giỏ hàng."""
    if request.user.is_authenticated:
        count = CartItem.objects.filter(account=request.user).count()
    else:
        count = 0
    return JsonResponse({'count': count})


def search_suggestions(request):
    """API tìm kiếm gợi ý sản phẩm (autocomplete)."""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'products': []})
    
    products = Product.objects.filter(
        is_available=True,
        name__icontains=query
    ).values('product_id', 'name', 'price', 'image_url', 'is_new', 'is_hot')[:8]
    
    results = []
    for p in products:
        results.append({
            'product_id': p['product_id'],
            'name': p['name'],
            'price': float(p['price']),
            'image_url': p['image_url'] or '',
            'is_new': p['is_new'],
            'is_hot': p['is_hot'],
        })
    
    return JsonResponse({'products': results})
