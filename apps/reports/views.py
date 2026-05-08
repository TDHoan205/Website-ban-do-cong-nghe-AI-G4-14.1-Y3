"""
Views cho app reports.
Báo cáo doanh thu, xuất Excel/PDF.
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate, TruncMonth, TruncWeek
from django.utils import timezone
from datetime import timedelta
import csv
import json

from apps.core.decorators import admin_required
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.users.models import Account


@admin_required
def revenue_report(request):
    """Báo cáo doanh thu."""
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    # Get date range filter
    period = request.GET.get('period', 'month')
    date_from = request.GET.get('date_from', start_of_month)
    date_to = request.GET.get('date_to', today)

    # Build queryset based on period
    orders_qs = Order.objects.filter(
        status__in=['Delivered', 'Shipped']
    )

    if period == 'week':
        date_from = today - timedelta(days=7)
        orders_qs = orders_qs.filter(order_date__date__gte=date_from)
    elif period == 'month':
        date_from = start_of_month
        orders_qs = orders_qs.filter(order_date__date__gte=date_from)
    elif period == 'quarter':
        date_from = today - timedelta(days=90)
        orders_qs = orders_qs.filter(order_date__date__gte=date_from)
    elif period == 'year':
        date_from = today.replace(month=1, day=1)
        orders_qs = orders_qs.filter(order_date__date__gte=date_from)
    else:
        if date_from:
            orders_qs = orders_qs.filter(order_date__date__gte=date_from)
        if date_to:
            orders_qs = orders_qs.filter(order_date__date__lte=date_to)

    # Summary stats
    total_revenue = orders_qs.aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = orders_qs.count()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    # Daily revenue
    daily_revenue = orders_qs.annotate(
        date=TruncDate('order_date')
    ).values('date').annotate(
        count=Count('id'),
        revenue=Sum('total_amount')
    ).order_by('date')

    # Top products
    top_products = OrderItem.objects.filter(
        order__in=orders_qs
    ).values(
        'product_id', 'product_name'
    ).annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum('subtotal')
    ).order_by('-total_revenue')[:10]

    # Order status breakdown
    status_breakdown = Order.objects.filter(
        order_date__date__gte=date_from,
        order_date__date__lte=date_to
    ).values('status').annotate(
        count=Count('id'),
        revenue=Sum('total_amount')
    ).order_by('status')

    context = {
        'page_title': 'Báo cáo doanh thu',
        'active_menu': 'reports',
        'period': period,
        'date_from': date_from,
        'date_to': date_to,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'daily_revenue': daily_revenue,
        'top_products': top_products,
        'status_breakdown': status_breakdown,
    }
    return render(request, 'reports/revenue_report.html', context)


@admin_required
def export_excel(request):
    """Xuất báo cáo Excel."""
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    period = request.GET.get('period', 'month')
    if period == 'week':
        date_from = today - timedelta(days=7)
    elif period == 'month':
        date_from = start_of_month
    elif period == 'quarter':
        date_from = today - timedelta(days=90)
    elif period == 'year':
        date_from = today.replace(month=1, day=1)
    else:
        date_from = start_of_month

    orders = Order.objects.filter(
        order_date__date__gte=date_from,
        order_date__date__lte=today,
        status__in=['Delivered', 'Shipped']
    ).select_related('account').order_by('-order_date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="report_{today}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Mã đơn', 'Khách hàng', 'Ngày đặt', 'Tổng tiền', 'Trạng thái'])

    for order in orders:
        writer.writerow([
            order.order_code,
            order.customer_name or order.account.username if order.account else 'Khách lẻ',
            order.order_date.strftime('%d/%m/%Y'),
            float(order.total_amount),
            order.get_status_display(),
        ])

    return response


@admin_required
def export_products_csv(request):
    """Xuất danh sách sản phẩm."""
    products = Product.objects.select_related('category', 'supplier').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Mã SP', 'Tên sản phẩm', 'Danh mục', 'Nhà cung cấp', 'Giá', 'Tồn kho', 'Trạng thái'])

    for p in products:
        writer.writerow([
            p.product_id,
            p.name,
            p.category.name if p.category else '',
            p.supplier.name if p.supplier else '',
            float(p.price),
            p.stock_quantity,
            'Còn hàng' if p.is_available else 'Hết hàng',
        ])

    return response


@admin_required
def export_orders_csv(request):
    """Xuất danh sách đơn hàng."""
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    orders = Order.objects.select_related('account').filter(
        order_date__date__gte=start_of_month,
        order_date__date__lte=today
    ).order_by('-order_date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Mã đơn', 'Khách hàng', 'SĐT', 'Địa chỉ', 'Ngày đặt', 'Tổng tiền', 'Trạng thái'])

    for o in orders:
        writer.writerow([
            o.order_code,
            o.customer_name or (o.account.username if o.account else 'Khách lẻ'),
            o.customer_phone or '',
            o.customer_address or '',
            o.order_date.strftime('%d/%m/%Y'),
            float(o.total_amount),
            o.get_status_display(),
        ])

    return response


@admin_required
def export_customers_csv(request):
    """Xuất danh sách khách hàng."""
    customers = Account.objects.filter(role='Customer').order_by('-created_at')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Mã KH', 'Username', 'Họ tên', 'Email', 'SĐT', 'Địa chỉ', 'Ngày đăng ký'])

    for c in customers:
        writer.writerow([
            c.account_id,
            c.username,
            c.full_name or '',
            c.email or '',
            c.phone or '',
            c.address or '',
            c.created_at.strftime('%d/%m/%Y'),
        ])

    return response
