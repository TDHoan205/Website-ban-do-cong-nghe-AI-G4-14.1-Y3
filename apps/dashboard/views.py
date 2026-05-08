"""
Views cho app dashboard.
Thống kê, biểu đồ, và báo cáo tổng quan.
"""
from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import timedelta
import json

from apps.core.decorators import admin_required
from apps.orders.models import Order
from apps.products.models import Product
from apps.users.models import Account
from apps.cart.models import CartItem
from apps.notifications.models import Notification


@admin_required
def dashboard_index(request):
    """Trang dashboard chính."""
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Order statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    processing_orders = Order.objects.filter(status__in=['Confirmed', 'Processing']).count()
    shipped_orders = Order.objects.filter(status='Shipped').count()
    completed_orders = Order.objects.filter(status='Delivered').count()
    cancelled_orders = Order.objects.filter(status='Cancelled').count()

    # Revenue statistics
    total_revenue = Order.objects.filter(
        status__in=['Delivered', 'Shipped']
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    today_revenue = Order.objects.filter(
        order_date__date=today,
        status__in=['Delivered', 'Shipped']
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    month_revenue = Order.objects.filter(
        order_date__date__gte=start_of_month,
        status__in=['Delivered', 'Shipped']
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Other statistics
    total_products = Product.objects.count()
    total_customers = Account.objects.filter(role='Customer').count()
    low_stock_products = Product.objects.filter(stock_quantity__lt=10).count()

    # Recent orders
    recent_orders = Order.objects.select_related('account').order_by('-order_date')[:5]

    # Top selling products (by order items)
    from apps.orders.models import OrderItem
    top_products = OrderItem.objects.values(
        'product_id', 'product_name'
    ).annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]

    # Orders by day (last 7 days)
    last_7_days = today - timedelta(days=6)
    orders_by_day = Order.objects.filter(
        order_date__date__gte=last_7_days
    ).annotate(
        date=TruncDate('order_date')
    ).values('date').annotate(
        count=Count('order_id'),
        revenue=Sum('total_amount')
    ).order_by('date')

    # Prepare chart data
    chart_labels = []
    chart_orders = []
    chart_revenue = []

    for i in range(7):
        day = last_7_days + timedelta(days=i)
        chart_labels.append(day.strftime('%d/%m'))
        
        day_data = next(
            (d for d in orders_by_day if d['date'] == day),
            None
        )
        chart_orders.append(day_data['count'] if day_data else 0)
        chart_revenue.append(float(day_data['revenue'] or 0) if day_data else 0)

    context = {
        'page_title': 'Dashboard',
        'active_menu': 'dashboard',
        # Stats cards
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'total_products': total_products,
        'total_customers': total_customers,
        'low_stock_products': low_stock_products,
        'system_notifications': Notification.objects.filter(is_read=False).count(),
        # Data
        'recent_orders': recent_orders,
        'top_products': top_products,
        # Chart
        'chart_labels': json.dumps(chart_labels),
        'chart_orders': json.dumps(chart_orders),
        'chart_revenue': json.dumps(chart_revenue),
    }
    return render(request, 'dashboard/index.html', context)


@admin_required
def reports(request):
    """Trang báo cáo thống kê."""
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    # Monthly orders
    monthly_orders = Order.objects.filter(
        order_date__date__gte=start_of_year
    ).annotate(
        month=TruncMonth('order_date')
    ).values('month').annotate(
        count=Count('order_id'),
        revenue=Sum('total_amount')
    ).order_by('month')

    monthly_labels = []
    monthly_revenue = []
    monthly_orders_count = []

    for item in monthly_orders:
        monthly_labels.append(item['month'].strftime('%B'))
        monthly_revenue.append(float(item['revenue'] or 0))
        monthly_orders_count.append(item['count'])

    context = {
        'page_title': 'Báo cáo thống kê',
        'active_menu': 'reports',
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_revenue': json.dumps(monthly_revenue),
        'monthly_orders': json.dumps(monthly_orders_count),
    }
    return render(request, 'dashboard/reports.html', context)
