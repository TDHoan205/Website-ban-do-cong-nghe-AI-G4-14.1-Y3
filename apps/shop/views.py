"""
Views cho app shop.
Frontend - Trang chu, danh sach san pham, chi tiet.
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models

from apps.products.models import Product, ProductVariant, ProductImage
from apps.categories.models import Category


def shop_home(request):
    """Trang chu shop - hien thi hero banner, danh muc, san pham."""
    categories = Category.objects.filter(is_active=True).order_by('display_order', 'name')[:8]

    per_page = 4

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

    deal_products = Product.objects.filter(
        is_available=True
    ).exclude(
        original_price__isnull=True
    ).exclude(
        original_price=0
    ).filter(
        original_price__gt=models.F('price')
    ).select_related('category').order_by('-discount_percent')[:3]

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
    """Trang danh sach san pham voi bo loc va phan trang."""
    products = Product.objects.filter(is_available=True).select_related('category')

    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    filter_type = request.GET.get('filter')
    if filter_type == 'new':
        products = products.filter(is_new=True)
    elif filter_type == 'hot':
        products = products.filter(is_hot=True)

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

    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

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
    """Trang chi tiet san pham."""
    product = get_object_or_404(
        Product.objects.select_related('category', 'supplier').prefetch_related(
            'variants', 'product_images'
        ),
        product_id=product_id
    )

    variants_qs = product.variants.filter(is_active=True).order_by('display_order', 'variant_name')
    images_qs = product.product_images.all()

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

    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(product_id=product_id).order_by('-rating')[:4]

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
    }
    return render(request, 'shop/product_detail.html', context)


def search_suggestions(request):
    """API tim kiem goi y san pham (autocomplete)."""
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


def privacy_policy(request):
    """Trang chinh sach bao mat."""
    return render(request, 'shop/privacy.html')


def terms_of_service(request):
    """Trang dieu khoan su dung."""
    return render(request, 'shop/terms.html')
