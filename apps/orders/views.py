"""
Views cho app orders.
CRUD cho Order, OrderItem, OrderStatusHistory models.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset, format_currency
from .models import Order, OrderItem, OrderStatusHistory
from .forms import OrderForm, OrderItemForm


@admin_required
def order_list(request):
    """Trang danh sach don hang."""
    orders = Order.objects.select_related('account').all().order_by('-order_date')

    search_query = request.GET.get('q', '')
    if search_query:
        orders = orders.filter(
            Q(order_code__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(customer_phone__icontains=search_query)
        )

    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        orders = orders.filter(order_date__date__gte=date_from)
    if date_to:
        orders = orders.filter(order_date__date__lte=date_to)

    page_obj, paginator = paginate_queryset(request, orders, 10)

    status_counts = Order.objects.values('status').annotate(count=Count('status'))

    context = {
        'page_title': 'Quan ly don hang',
        'active_menu': 'orders',
        'orders': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
        'order_statuses': Order.STATUS_CHOICES,
        'status_counts': {item['status'].lower(): item['count'] for item in status_counts},
    }
    return render(request, 'orders/order_list.html', context)


@admin_required
def order_detail(request, pk):
    """Chi tiet don hang voi lich su trang thai."""
    order = get_object_or_404(
        Order.objects.prefetch_related('items', 'items__product', 'status_history', 'status_history__changed_by'),
        pk=pk
    )
    status_history = order.status_history.all().order_by('-created_at')

    context = {
        'page_title': f'Don hang {order.order_code}',
        'active_menu': 'orders',
        'order': order,
        'status_history': status_history,
        'order_statuses': Order.STATUS_CHOICES,
        'payment_statuses': Order.PAYMENT_STATUS_CHOICES,
    }
    return render(request, 'orders/order_detail.html', context)


@admin_required
def order_create(request):
    """Tao don hang moi (admin)."""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            OrderStatusHistory.objects.create(
                order=order,
                old_status=None,
                new_status=order.status,
                changed_by=request.user,
                notes='Don hang duoc tao boi admin.'
            )
            messages.success(request, f'Tao don hang "{order.order_code}" thanh cong!')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = OrderForm()

    context = {
        'page_title': 'Tao don hang moi',
        'active_menu': 'orders',
        'form': form,
    }
    return render(request, 'orders/order_form.html', context)


@admin_required
def order_update(request, pk):
    """Cap nhat thong tin don hang."""
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cap nhat don hang thanh cong!')
            return redirect('orders:order_detail', pk=pk)
    else:
        form = OrderForm(instance=order)

    context = {
        'page_title': f'Sua don hang {order.order_code}',
        'active_menu': 'orders',
        'form': form,
        'order': order,
    }
    return render(request, 'orders/order_form.html', context)


@admin_required
@require_http_methods(['POST'])
def order_update_status(request, pk):
    """Cap nhat trang thai don hang (AJAX) + ghi lich su."""
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    notes = request.POST.get('notes', '')

    if new_status not in dict(Order.STATUS_CHOICES):
        return JsonResponse({
            'success': False,
            'message': 'Trang thai khong hop le!'
        })

    old_status = order.status
    order.status = new_status
    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        old_status=old_status,
        new_status=new_status,
        changed_by=request.user,
        notes=notes
    )

    status_display = dict(Order.STATUS_CHOICES).get(new_status, new_status)

    return JsonResponse({
        'success': True,
        'message': f'Cap nhat trang thai thanh "{status_display}"!',
        'status': new_status,
        'status_display': status_display,
    })


@admin_required
@require_http_methods(['POST'])
def order_update_payment_status(request, pk):
    """Cap nhat trang thai thanh toan (AJAX)."""
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('payment_status')

    if new_status not in dict(Order.PAYMENT_STATUS_CHOICES):
        return JsonResponse({
            'success': False,
            'message': 'Trang thai thanh toan khong hop le!'
        })

    old_status = order.payment_status
    order.payment_status = new_status
    order.save()

    return JsonResponse({
        'success': True,
        'message': f'Cap nhat thanh toan thanh "{dict(Order.PAYMENT_STATUS_CHOICES).get(new_status)}"!',
        'payment_status': new_status,
    })


@admin_required
@require_http_methods(['POST'])
def order_update_admin_notes(request, pk):
    """Cap nhat ghi chu admin (AJAX)."""
    order = get_object_or_404(Order, pk=pk)
    admin_notes = request.POST.get('admin_notes', '')
    order.admin_notes = admin_notes
    order.save()
    return JsonResponse({
        'success': True,
        'message': 'Cap nhat ghi chu thanh cong!'
    })


@admin_required
@require_http_methods(['POST'])
def order_cancel(request, pk):
    """Huy don hang."""
    order = get_object_or_404(Order, pk=pk)

    if not order.can_cancel:
        return JsonResponse({
            'success': False,
            'message': 'Khong the huy don hang o trang thai nay!'
        })

    old_status = order.status
    order.status = 'Cancelled'
    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        old_status=old_status,
        new_status='Cancelled',
        changed_by=request.user,
        notes='Don hang bi huy boi admin.'
    )

    return JsonResponse({
        'success': True,
        'message': 'Huy don hang thanh cong!'
    })


@admin_required
@require_http_methods(['POST'])
def order_confirm_payment(request, pk):
    """Xac nhan thanh toan (chuyen tu AwaitingConfirmation sang Paid)."""
    order = get_object_or_404(Order, pk=pk)

    if order.payment_status != 'AwaitingConfirmation':
        return JsonResponse({
            'success': False,
            'message': 'Don hang khong o trang thai cho xac nhan thanh toan!'
        })

    old_status = order.payment_status
    order.payment_status = 'Paid'
    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        old_status=old_status,
        new_status='Paid',
        changed_by=request.user,
        notes='Xac nhan thanh toan thu cong.'
    )

    return JsonResponse({
        'success': True,
        'message': 'Xac nhan thanh toan thanh cong!'
    })


@admin_required
@require_http_methods(['POST'])
def order_reject_payment(request, pk):
    """Tu choi thanh toan."""
    order = get_object_or_404(Order, pk=pk)
    reason = request.POST.get('reason', '')

    if order.payment_status != 'AwaitingConfirmation':
        return JsonResponse({
            'success': False,
            'message': 'Don hang khong o trang thai cho xac nhan thanh toan!'
        })

    old_status = order.payment_status
    order.payment_status = 'Failed'
    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        old_status=old_status,
        new_status='Failed',
        changed_by=request.user,
        notes=f'Tu choi thanh toan. Ly do: {reason}' if reason else 'Tu choi thanh toan.'
    )

    return JsonResponse({
        'success': True,
        'message': 'Tu choi thanh toan thanh cong!'
    })


# =====================
# Order Statistics API
# =====================

@admin_required
def order_statistics(request):
    """API lay thong ke don hang."""
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    stats = {
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='Pending').count(),
        'processing_orders': Order.objects.filter(status__in=['Confirmed', 'Processing']).count(),
        'completed_orders': Order.objects.filter(status__in=['Delivered', 'Shipped']).count(),
        'cancelled_orders': Order.objects.filter(status='Cancelled').count(),
        'today_orders': Order.objects.filter(order_date__date=today).count(),
        'week_orders': Order.objects.filter(order_date__date__gte=start_of_week).count(),
        'month_orders': Order.objects.filter(order_date__date__gte=start_of_month).count(),
        'awaiting_payment': Order.objects.filter(payment_status='AwaitingConfirmation').count(),
        'total_revenue': Order.objects.filter(
            status__in=['Delivered', 'Shipped'],
            payment_status='Paid'
        ).aggregate(total=Sum('total_amount'))['total'] or 0,
        'today_revenue': Order.objects.filter(
            order_date__date=today,
            status__in=['Delivered', 'Shipped'],
            payment_status='Paid'
        ).aggregate(total=Sum('total_amount'))['total'] or 0,
    }

    return JsonResponse({'success': True, 'data': stats})


# =====================
# Public: Order History (Customer)
# =====================

def order_history(request):
    """Trang lich su don hang cua khach hang."""
    if not request.user.is_authenticated:
        messages.warning(request, 'Vui long dang nhap de xem lich su don hang.')
        return redirect('accounts:login')

    orders = Order.objects.filter(
        account=request.user
    ).order_by('-order_date')

    search_query = request.GET.get('q', '')
    if search_query:
        orders = orders.filter(
            Q(order_code__icontains=search_query) |
            Q(customer_name__icontains=search_query)
        )

    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    page_obj, paginator = paginate_queryset(request, orders, 10)

    context = {
        'orders': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'status_filter': status_filter,
        'order_statuses': Order.STATUS_CHOICES,
    }
    return render(request, 'orders/order_history.html', context)


def order_tracking(request):
    """Tra cuu don hang bang ma don hoac SDT (khong can dang nhap)."""
    order = None
    error = None

    if request.method == 'GET':
        order_code = request.GET.get('order_code', '').strip()
        phone = request.GET.get('phone', '').strip()

        if order_code and phone:
            order = Order.objects.filter(
                order_code__icontains=order_code,
                customer_phone=phone
            ).first()

            if not order:
                error = 'Khong tim thay don hang voi ma va so dien thoai nay.'
        elif order_code and not phone:
            error = 'Vui long nhap so dien thoai de tra cuu.'
        elif phone and not order_code:
            error = 'Vui long nhap ma don hang de tra cuu.'

    context = {
        'order': order,
        'error': error,
        'order_code': request.GET.get('order_code', ''),
        'phone': request.GET.get('phone', ''),
        'order_statuses': Order.STATUS_CHOICES,
    }
    return render(request, 'orders/order_tracking.html', context)
