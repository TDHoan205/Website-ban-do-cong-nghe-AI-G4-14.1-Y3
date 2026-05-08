"""
Context processors cho toàn bộ ứng dụng.
"""
from django.core.cache import cache


def admin_notifications(request):
    """Cung cấp thông báo cho header admin."""
    # Kiểm tra request.user tồn tại và được xác thực
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {}

    try:
        from apps.notifications.models import Notification
        unread_count = cache.get(f'notif_unread_{request.user.pk}', None)
        if unread_count is None:
            unread_count = Notification.objects.filter(
                account=request.user,
                is_read=False
            ).count()
            cache.set(f'notif_unread_{request.user.pk}', unread_count, 300)

        recent = list(Notification.objects.filter(
            account=request.user
        ).order_by('-created_at')[:5].values(
            'notification_id', 'title', 'type', 'link', 'created_at', 'is_read'
        ))

        return {
            'unread_notifications': unread_count,
            'recent_notifications': recent,
        }
    except Exception:
        return {
            'unread_notifications': 0,
            'recent_notifications': [],
        }
