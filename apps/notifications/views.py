"""
Views cho app notifications.
Quản lý thông báo.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset
from apps.users.models import Account
from .models import Notification


@admin_required
def notification_list(request):
    """Trang danh sách thông báo."""
    notifications = Notification.objects.select_related('account').all().order_by('-created_at')

    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        notifications = notifications.filter(type=type_filter)

    # Filter by read status
    read_filter = request.GET.get('read')
    if read_filter == 'read':
        notifications = notifications.filter(is_read=True)
    elif read_filter == 'unread':
        notifications = notifications.filter(is_read=False)

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        notifications = notifications.filter(
            Q(title__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(account__username__icontains=search_query)
        )

    # Paginate
    page_obj, paginator = paginate_queryset(request, notifications, 5)

    # Counts
    unread_count = Notification.objects.filter(is_read=False).count()

    context = {
        'page_title': 'Quản lý thông báo',
        'active_menu': 'notifications',
        'notifications': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'type_filter': type_filter,
        'read_filter': read_filter,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/notification_list.html', context)


@admin_required
def notification_create_all(request):
    """Tạo thông báo gửi tất cả users."""
    from .forms import NotificationForm

    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification_type = form.cleaned_data['notification_type']
            title = form.cleaned_data['title']
            message_content = form.cleaned_data['message']
            link = form.cleaned_data.get('link', '')

            customers = Account.objects.filter(role='Customer', is_active=True)
            for customer in customers:
                Notification.objects.create(
                    account=customer,
                    type=notification_type,
                    title=title,
                    message=message_content,
                    link=link
                )
            messages.success(request, f'Đã gửi thông báo đến {customers.count()} khách hàng!')
            return redirect('notifications:notification_list')
    else:
        form = NotificationForm()

    context = {
        'page_title': 'Gửi thông báo',
        'active_menu': 'notifications',
        'form': form,
    }
    return render(request, 'notifications/notification_form.html', context)


@admin_required
@require_http_methods(['POST'])
def notification_mark_read(request, pk):
    """Đánh dấu đã đọc."""
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()
    return JsonResponse({'success': True})


@admin_required
@require_http_methods(['POST'])
def notification_mark_all_read(request):
    """Đánh dấu tất cả đã đọc."""
    Notification.objects.filter(is_read=False).update(is_read=True)
    return JsonResponse({'success': True, 'message': 'Đã đánh dấu tất cả là đã đọc!'})


@admin_required
@require_http_methods(['POST'])
def notification_delete(request, pk):
    """Xóa thông báo."""
    notification = get_object_or_404(Notification, pk=pk)
    notification.delete()
    return JsonResponse({'success': True, 'message': 'Đã xóa thông báo!'})


@admin_required
@require_http_methods(['POST'])
def notification_delete_all(request):
    """Xóa tất cả thông báo đã đọc."""
    deleted_count, _ = Notification.objects.filter(is_read=True).delete()
    return JsonResponse({'success': True, 'message': f'Đã xóa {deleted_count} thông báo!'})


@admin_required
def get_unread_count(request):
    """API lấy số thông báo chưa đọc."""
    count = Notification.objects.filter(is_read=False).count()
    return JsonResponse({'count': count})
