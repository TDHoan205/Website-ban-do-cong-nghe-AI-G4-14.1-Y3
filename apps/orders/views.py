"""
Views cho app orders.
CRUD cho Order, OrderItem models với AJAX status management.
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
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm


@admin_required
def order_list(request):
    """Trang danh sách đơn hàng."""
    orders = Order.objects.select_related('account').all().order_by('-order_date')

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        orders = orders.filter(
            Q(order_code__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(customer_phone__icontains=search_query)
        )

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        orders = orders.filter(order_date__date__gte=date_from)
    if date_to:
        orders = orders.filter(order_date__date__lte=date_to)

    # Paginate
    page_obj, paginator = paginate_queryset(request, orders, 5)

    # Status counts for filter tabs
    status_counts = Order.objects.values('status').annotate(count=Count('status'))

    context = {
        'page_title': 'Quản lý đơn hàng',
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
    """Chi tiết đơn hàng."""
    order = get_object_or_404(Order.objects.prefetch_related('items', 'items__product'), pk=pk)

    context = {
        'page_title': f'Đơn hàng {order.order_code}',
        'active_menu': 'orders',
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@admin_required
def order_create(request):
    """Tạo đơn hàng mới (admin)."""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            messages.success(request, f'Tạo đơn hàng "{order.order_code}" thành công!')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = OrderForm()

    context = {
        'page_title': 'Tạo đơn hàng mới',
        'active_menu': 'orders',
        'form': form,
    }
    return render(request, 'orders/order_form.html', context)


@admin_required
def order_update(request, pk):
    """Cập nhật thông tin đơn hàng."""
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cập nhật đơn hàng thành công!')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)

    context = {
        'page_title': f'Sửa đơn hàng {order.order_code}',
        'active_menu': 'orders',
        'form': form,
        'order': order,
    }
    return render(request, 'orders/order_form.html', context)


@admin_required
@require_http_methods(['POST'])
def order_update_status(request, pk):
    """Cập nhật trạng thái đơn hàng (AJAX)."""
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')

    if new_status not in dict(Order.STATUS_CHOICES):
        return JsonResponse({
            'success': False,
            'message': 'Trạng thái không hợp lệ!'
        })

    old_status = order.status
    order.status = new_status
    order.save()

    status_display = dict(Order.STATUS_CHOICES).get(new_status, new_status)

    return JsonResponse({
        'success': True,
        'message': f'Cập nhật trạng thái thành "{status_display}"!',
        'status': new_status,
        'status_display': status_display,
    })


@admin_required
@require_http_methods(['POST'])
def order_cancel(request, pk):
    """Hủy đơn hàng."""
    order = get_object_or_404(Order, pk=pk)

    if not order.can_cancel:
        return JsonResponse({
            'success': False,
            'message': 'Không thể hủy đơn hàng ở trạng thái này!'
        })

    order.status = 'Cancelled'
    order.save()

    return JsonResponse({
        'success': True,
        'message': 'Hủy đơn hàng thành công!'
    })


# =====================
# Order Statistics API
# =====================

@admin_required
def order_statistics(request):
    """API lấy thống kê đơn hàng."""
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
        'total_revenue': Order.objects.filter(status__in=['Delivered', 'Shipped']).aggregate(
            total=Sum('total_amount'))['total'] or 0,
        'today_revenue': Order.objects.filter(
            order_date__date=today,
            status__in=['Delivered', 'Shipped']
        ).aggregate(total=Sum('total_amount'))['total'] or 0,
    }

    return JsonResponse({'success': True, 'data': stats})
