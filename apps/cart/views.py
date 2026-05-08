"""
Views cho app cart.
CRUD cho CartItem model và checkout.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Q
from django.db import transaction
from django.utils import timezone

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset, generate_order_code
from apps.products.models import Product, ProductVariant
from apps.users.models import Account
from apps.orders.models import Order, OrderItem
from .models import CartItem


# =====================
# Public Cart Views (Shop)
# =====================

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
    
    # Xử lý khi submit form thanh toán
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '')
        customer_phone = request.POST.get('customer_phone', '')
        customer_address = request.POST.get('customer_address', '')
        notes = request.POST.get('notes', '')
        
        if not customer_name or not customer_phone or not customer_address:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin giao hàng!')
        else:
            with transaction.atomic():
                # Tạo đơn hàng
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
                
                # Tạo order items
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
                    
                    # Cập nhật tồn kho
                    if item.variant:
                        item.variant.stock_quantity = max(0, item.variant.stock_quantity - item.quantity)
                        item.variant.save()
                    else:
                        item.product.stock_quantity = max(0, item.product.stock_quantity - item.quantity)
                        item.product.save()
                
                # Xóa giỏ hàng
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


@require_http_methods(['POST'])
def add_to_cart_api(request):
    """API thêm vào giỏ hàng."""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'Vui lòng đăng nhập!',
            'requires_login': True
        })
    
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
    
    cart_count = CartItem.objects.filter(account=request.user).count()
    
    return JsonResponse({
        'success': True,
        'message': 'Đã thêm sản phẩm vào giỏ hàng!',
        'cart_count': cart_count,
        'quantity': cart_item.quantity
    })


# =====================
# Admin Cart Views
# =====================

@admin_required
def cart_list(request):
    """Trang danh sách giỏ hàng (admin view all carts)."""
    cart_items = CartItem.objects.select_related(
        'account', 'product', 'variant'
    ).all().order_by('-added_date')

    # Search by account
    search_query = request.GET.get('q', '')
    if search_query:
        cart_items = cart_items.filter(
            Q(account__username__icontains=search_query) |
            Q(account__full_name__icontains=search_query) |
            Q(product__name__icontains=search_query)
        )

    # Filter by account
    account_filter = request.GET.get('account')
    if account_filter:
        cart_items = cart_items.filter(account_id=account_filter)

    # Paginate
    page_obj, paginator = paginate_queryset(request, cart_items, 20)

    # Get accounts for filter
    accounts = Account.objects.filter(
        cart_items__isnull=False
    ).distinct().order_by('username')

    context = {
        'page_title': 'Quản lý giỏ hàng',
        'active_menu': 'cart',
        'cart_items': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'account_filter': account_filter,
        'accounts': accounts,
    }
    return render(request, 'cart/cart_list.html', context)


@admin_required
def cart_detail(request, account_pk):
    """Chi tiết giỏ hàng của 1 khách hàng."""
    account = get_object_or_404(Account, pk=account_pk)
    cart_items = CartItem.objects.filter(
        account=account
    ).select_related('product', 'variant').order_by('-added_date')

    total = cart_items.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    context = {
        'page_title': f'Giỏ hàng - {account.username}',
        'active_menu': 'cart',
        'account': account,
        'cart_items': cart_items,
        'total_items': total,
    }
    return render(request, 'cart/cart_detail.html', context)


@admin_required
@require_http_methods(['POST'])
def cart_add(request):
    """Thêm sản phẩm vào giỏ hàng của khách (admin)."""
    account_id = request.POST.get('account_id')
    product_id = request.POST.get('product_id')
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))

    if not account_id or not product_id:
        return JsonResponse({
            'success': False,
            'message': 'Thiếu thông tin!'
        })

    # Check existing
    existing = CartItem.objects.filter(
        account_id=account_id,
        product_id=product_id,
        variant_id=variant_id or None
    ).first()

    if existing:
        existing.quantity += quantity
        existing.save()
        message = 'Cập nhật số lượng thành công!'
    else:
        CartItem.objects.create(
            account_id=account_id,
            product_id=product_id,
            variant_id=variant_id or None,
            quantity=quantity
        )
        message = 'Thêm vào giỏ hàng thành công!'

    return JsonResponse({'success': True, 'message': message})


@admin_required
@require_http_methods(['POST'])
def cart_update(request, pk):
    """Cập nhật số lượng."""
    cart_item = get_object_or_404(CartItem, pk=pk)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        cart_item.delete()
        return JsonResponse({'success': True, 'message': 'Đã xóa khỏi giỏ hàng!'})

    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({
        'success': True,
        'message': 'Cập nhật thành công!',
        'subtotal': float(cart_item.subtotal)
    })


@admin_required
@require_http_methods(['POST'])
def cart_remove(request, pk):
    """Xóa item khỏi giỏ hàng."""
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return JsonResponse({'success': True, 'message': 'Đã xóa khỏi giỏ hàng!'})
