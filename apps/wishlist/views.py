"""
Views cho app wishlist.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from apps.products.models import Product
from .models import Wishlist, WishlistItem, RecentlyViewed


@login_required
def wishlist_view(request):
    """Trang danh sach yeu thich."""
    wishlist, _ = Wishlist.objects.get_or_create(account=request.user)
    items = wishlist.items.select_related('product', 'product__category').all()

    context = {
        'wishlist_items': items,
        'total_items': items.count(),
    }
    return render(request, 'wishlist/wishlist.html', context)


@login_required
@require_http_methods(["POST"])
def add_to_wishlist(request):
    """API them san pham vao wishlist."""
    product_id = request.POST.get('product_id')

    try:
        product = Product.objects.get(product_id=product_id, is_available=True)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'San pham khong ton tai.'})

    wishlist, _ = Wishlist.objects.get_or_create(account=request.user)

    item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )

    if not created:
        return JsonResponse({
            'success': False,
            'message': 'San pham da co trong danh sach yeu thich.',
            'already_exists': True
        })

    count = wishlist.items.count()
    return JsonResponse({
        'success': True,
        'message': 'Da them vao danh sach yeu thich!',
        'count': count
    })


@login_required
@require_http_methods(["POST"])
def remove_from_wishlist(request):
    """API xoa san pham khoi wishlist."""
    product_id = request.POST.get('product_id')

    try:
        wishlist = Wishlist.objects.get(account=request.user)
        item = WishlistItem.objects.get(wishlist=wishlist, product_id=product_id)
        item.delete()
        count = wishlist.items.count()
        return JsonResponse({
            'success': True,
            'message': 'Da xoa khoi danh sach yeu thich.',
            'count': count
        })
    except (Wishlist.DoesNotExist, WishlistItem.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'San pham khong co trong wishlist.'})


@login_required
@require_http_methods(["GET"])
def get_wishlist_count(request):
    """API lay so luong wishlist."""
    try:
        wishlist = Wishlist.objects.get(account=request.user)
        return JsonResponse({'success': True, 'count': wishlist.items.count()})
    except Wishlist.DoesNotExist:
        return JsonResponse({'success': True, 'count': 0})


@login_required
@require_http_methods(["GET"])
def get_recently_viewed(request):
    """API lay danh sach san pham da xem."""
    recent = RecentlyViewed.objects.filter(
        account=request.user
    ).select_related('product', 'product__category')[:12]

    items = [
        {
            'product_id': rv.product.product_id,
            'name': rv.product.name,
            'price': float(rv.product.price),
            'image_url': rv.product.image_url or '',
            'viewed_at': rv.viewed_at.isoformat(),
        }
        for rv in recent
    ]

    return JsonResponse({'success': True, 'items': items})


@login_required
@require_http_methods(["POST"])
def track_viewed(request):
    """API ghi nhan san pham da xem (goi khi xem chi tiet san pham)."""
    product_id = request.POST.get('product_id')

    try:
        product = Product.objects.get(product_id=product_id, is_available=True)
    except Product.DoesNotExist:
        return JsonResponse({'success': False})

    rv, created = RecentlyViewed.objects.get_or_create(
        account=request.user,
        product=product
    )

    if not created:
        rv.save()

    RecentlyViewed.objects.filter(account=request.user).exclude(
        product_id=product_id
    ).order_by('-viewed_at')[20:].delete()

    return JsonResponse({'success': True})
