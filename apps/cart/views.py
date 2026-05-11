"""
Views cho app cart.
CRUD cho CartItem model va checkout, ho tro ca guest va member.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Q
from django.db import transaction
from django.utils import timezone
from django.conf import settings

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset, generate_order_code
from apps.products.models import Product, ProductVariant
from apps.users.models import Account
from apps.orders.models import Order, OrderItem
from .models import CartItem


def _get_cart_key(request):
    """Lay session key cho guest cart."""
    if request.session.session_key is None:
        request.session.create()
    return request.session.session_key


def _get_cart_items(request):
    """Lay gio hang phu hop: account neu dang nhap, session neu guest."""
    if request.user.is_authenticated:
        return CartItem.objects.filter(account=request.user)
    else:
        session_key = _get_cart_key(request)
        return CartItem.objects.filter(session_key=session_key)


def _merge_guest_cart(request, user):
    """Gop gio hang cua guest vao tai khoan khi dang nhap."""
    session_key = _get_cart_key(request)
    guest_items = CartItem.objects.filter(session_key=session_key)

    for guest_item in guest_items:
        existing = CartItem.objects.filter(
            account=user,
            product=guest_item.product,
            variant=guest_item.variant
        ).first()

        if existing:
            existing.quantity += guest_item.quantity
            max_stock = guest_item.variant.stock_quantity if guest_item.variant else guest_item.product.stock_quantity
            if existing.quantity > max_stock:
                existing.quantity = max_stock
            existing.save()
        else:
            CartItem.objects.create(
                account=user,
                product=guest_item.product,
                variant=guest_item.variant,
                quantity=guest_item.quantity
            )

        guest_item.delete()


# =====================
# Public Cart Views (Shop)
# =====================

def cart_view(request):
    """Trang gio hang - ho tro ca guest va member."""
    cart_items = _get_cart_items(request).select_related('product', 'variant')

    # Tinh tong tien
    total = sum(item.subtotal for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
        'total_items': total_items,
        'is_guest': not request.user.is_authenticated,
    }
    return render(request, 'shop/cart.html', context)


def checkout_view(request):
    """Trang thanh toan - ho tro ca guest va member."""
    all_cart_items = _get_cart_items(request).select_related('product', 'variant')

    if not all_cart_items.exists():
        messages.warning(request, 'Gio hang trong!')
        return redirect('shop:cart')

    # Loc items da chon tu POST (gui tu cart.html goCheckout)
    selected_ids = request.POST.getlist('selected_items') if request.method == 'POST' else []

    if selected_ids:
        cart_items = all_cart_items.filter(cart_item_id__in=selected_ids)
    else:
        cart_items = all_cart_items

    if not cart_items.exists():
        messages.warning(request, 'Gio hang trong hoac khong co san pham nao duoc chon!')
        return redirect('shop:cart')

    total = sum(item.subtotal for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    # Tinh phi ship
    shipping_fee = 30000 if total < 500000 else 0
    final_total = total + shipping_fee

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        customer_address = request.POST.get('customer_address', '').strip()
        notes = request.POST.get('notes', '').strip()
        payment_method = request.POST.get('payment_method', 'COD').strip()

        if not customer_name or not customer_phone or not customer_address:
            messages.error(request, 'Vui long dien day du thong tin giao hang!')
        else:
            with transaction.atomic():
                order = Order.objects.create(
                    account=request.user if request.user.is_authenticated else None,
                    order_code=generate_order_code(),
                    total_amount=final_total,
                    shipping_fee=shipping_fee,
                    status='Pending',
                    customer_name=customer_name,
                    customer_phone=customer_phone,
                    customer_address=customer_address,
                    notes=notes,
                    payment_method=payment_method,
                    payment_status='Pending',
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

                messages.success(request, f'Dat hang thanh cong! Ma don hang: {order.order_code}')
                return redirect('orders:order_detail', pk=order.pk)

    context = {
        'cart_items': cart_items,
        'total': total,
        'total_items': total_items,
        'shipping_fee': shipping_fee,
        'final_total': final_total,
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'shop/checkout.html', context)


@require_http_methods(["POST"])
def add_to_cart_api(request):
    """API them vao gio hang - ho tro ca guest va member."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    variant_id = request.POST.get('variant_id')

    try:
        product = Product.objects.get(product_id=product_id, is_available=True)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'San pham khong ton tai.'})

    variant = None
    if variant_id:
        try:
            variant = ProductVariant.objects.get(variant_id=variant_id, is_active=True)
        except ProductVariant.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Bien the khong ton tai.'})

    # Kiem tra ton kho
    if variant:
        stock = variant.stock_quantity
    else:
        stock = product.stock_quantity

    if quantity > stock:
        return JsonResponse({
            'success': False,
            'message': f'San pham chi con {stock} trong kho.'
        })

    # Lay cart_key: account hoac session
    account = request.user if request.user.is_authenticated else None
    session_key = _get_cart_key(request) if not account else None

    # Kiem tra da co trong gio chua
    if account:
        cart_item = CartItem.objects.filter(
            account=account,
            product=product,
            variant=variant
        ).first()
    else:
        cart_item = CartItem.objects.filter(
            session_key=session_key,
            product=product,
            variant=variant
        ).first()

    if cart_item:
        cart_item.quantity += quantity
        if cart_item.quantity > stock:
            cart_item.quantity = stock
        cart_item.save()
    else:
        cart_item = CartItem.objects.create(
            account=account,
            session_key=session_key,
            product=product,
            variant=variant,
            quantity=quantity
        )

    cart_count = _get_cart_items(request).count()

    return JsonResponse({
        'success': True,
        'message': 'Da them san pham vao gio hang!',
        'cart_count': cart_count,
        'quantity': cart_item.quantity
    })


@require_http_methods(["GET"])
def get_cart_count_api(request):
    """API lay so luong san pham trong gio hang."""
    count = _get_cart_items(request).count()
    return JsonResponse({'success': True, 'count': count})


@require_http_methods(["POST"])
def update_cart_api(request):
    """API cap nhat so luong gio hang."""
    cart_item_id = request.POST.get('cart_item_id')
    quantity = int(request.POST.get('quantity', 1))

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(cart_item_id=cart_item_id, account=request.user)
        else:
            session_key = _get_cart_key(request)
            cart_item = CartItem.objects.get(cart_item_id=cart_item_id, session_key=session_key)
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'San pham khong co trong gio hang.'})

    if quantity <= 0:
        cart_item.delete()
        return JsonResponse({
            'success': True,
            'message': 'Da xoa san pham khoi gio hang.',
            'deleted': True
        })

    # Kiem tra ton kho
    stock = cart_item.variant.stock_quantity if cart_item.variant_id else cart_item.product.stock_quantity
    if quantity > stock:
        return JsonResponse({
            'success': False,
            'message': f'Chi con {stock} san pham trong kho.',
            'quantity': cart_item.quantity
        })

    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({
        'success': True,
        'message': 'Da cap nhat so luong.',
        'quantity': quantity,
        'subtotal': str(cart_item.subtotal)
    })


@require_http_methods(["POST"])
def remove_cart_api(request):
    """API xoa san pham khoi gio hang."""
    cart_item_id = request.POST.get('cart_item_id')

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(cart_item_id=cart_item_id, account=request.user)
        else:
            session_key = _get_cart_key(request)
            cart_item = CartItem.objects.get(cart_item_id=cart_item_id, session_key=session_key)
        cart_item.delete()

        remaining_items = _get_cart_items(request)
        total = sum(item.subtotal for item in remaining_items)

        return JsonResponse({
            'success': True,
            'message': 'Da xoa san pham khoi gio hang.',
            'cart_count': remaining_items.count(),
            'total': str(total)
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'San pham khong co trong gio hang.'})


# =====================
# Admin Cart Views
# =====================

@admin_required
def cart_list(request):
    """Trang danh sach gio hang (admin view all carts)."""
    cart_items = CartItem.objects.select_related(
        'account', 'product', 'variant'
    ).all().order_by('-added_date')

    search_query = request.GET.get('q', '')
    if search_query:
        cart_items = cart_items.filter(
            Q(account__username__icontains=search_query) |
            Q(account__full_name__icontains=search_query) |
            Q(product__name__icontains=search_query)
        )

    account_filter = request.GET.get('account')
    if account_filter:
        cart_items = cart_items.filter(account_id=account_filter)

    page_obj, paginator = paginate_queryset(request, cart_items, 20)

    accounts = Account.objects.filter(
        cart_items__isnull=False
    ).distinct().order_by('username')

    context = {
        'page_title': 'Quan ly gio hang',
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
    """Chi tiet gio hang cua 1 khach hang."""
    account = get_object_or_404(Account, pk=account_pk)
    cart_items = CartItem.objects.filter(
        account=account
    ).select_related('product', 'variant').order_by('-added_date')

    total = cart_items.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    context = {
        'page_title': f'Gio hang - {account.username}',
        'active_menu': 'cart',
        'account': account,
        'cart_items': cart_items,
        'total_items': total,
    }
    return render(request, 'cart/cart_detail.html', context)


@admin_required
@require_http_methods(['POST'])
def cart_add(request):
    """Them san pham vao gio hang cua khach (admin)."""
    account_id = request.POST.get('account_id')
    product_id = request.POST.get('product_id')
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))

    if not account_id or not product_id:
        return JsonResponse({
            'success': False,
            'message': 'Thieu thong tin!'
        })

    existing = CartItem.objects.filter(
        account_id=account_id,
        product_id=product_id,
        variant_id=variant_id or None
    ).first()

    if existing:
        existing.quantity += quantity
        existing.save()
        message = 'Cap nhat so luong thanh cong!'
    else:
        CartItem.objects.create(
            account_id=account_id,
            product_id=product_id,
            variant_id=variant_id or None,
            quantity=quantity
        )
        message = 'Them vao gio hang thanh cong!'

    return JsonResponse({'success': True, 'message': message})


@admin_required
@require_http_methods(['POST'])
def cart_update(request, pk):
    """Cap nhat so luong."""
    cart_item = get_object_or_404(CartItem, pk=pk)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        cart_item.delete()
        return JsonResponse({'success': True, 'message': 'Da xoa khoi gio hang!'})

    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({
        'success': True,
        'message': 'Cap nhat thanh cong!',
        'subtotal': float(cart_item.subtotal)
    })


@admin_required
@require_http_methods(['POST'])
def cart_remove(request, pk):
    """Xoa item khoi gio hang."""
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return JsonResponse({'success': True, 'message': 'Da xoa khoi gio hang!'})
