"""
Utility functions for the application.
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_queryset(request, queryset, per_page=10):
    """
    Paginate a queryset and return paginated results.
    Usage in view:
        page_obj, paginator = paginate_queryset(request, Product.objects.all(), 10)
    """
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    return paginated_queryset, paginator


def format_currency(amount):
    """
    Format amount as Vietnamese currency.
    Usage: {{ product.price|format_currency }}
    """
    try:
        return f"{float(amount):,.0f} đ".replace(",", ".")
    except (ValueError, TypeError):
        return "0 đ"


def generate_order_code():
    """
    Generate a unique order code.
    Usage: order_code = generate_order_code()
    """
    import random
    import string
    from datetime import datetime
    prefix = datetime.now().strftime('%Y%m%d')
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD-{prefix}-{suffix}"
