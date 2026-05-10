"""
Views cho app chat.
Quản lý phiên chat, tin nhắn, và log AI.
"""
import uuid
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count
from django.utils import timezone

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset
from apps.users.models import Account
from .models import ChatSession, ChatMessage, AIConversationLog
from .services.ai_service import ai_service

logger = logging.getLogger(__name__)

INTENT_CHOICES = [
    ('greeting', 'Chào hỏi'),
    ('thanks', 'Cảm ơn'),
    ('product_inquiry', 'Tư vấn sản phẩm'),
    ('price_inquiry', 'Hỏi giá'),
    ('order_status', 'Tình trạng đơn'),
    ('return_policy', 'Đổi trả'),
    ('payment', 'Thanh toán'),
    ('shipping', 'Giao hàng'),
    ('contact', 'Liên hệ'),
    ('specs', 'Thông số kỹ thuật'),
    ('cart_order', 'Đặt hàng'),
    ('complaint', 'Phàn nàn'),
    ('unknown', 'Không xác định'),
]


@admin_required
def chat_analytics(request):
    """Dashboard phân tích chat AI."""
    from django.db.models import Count, Avg
    from django.db.models.functions import TruncDate
    from django.utils import timezone
    from datetime import timedelta

    time_range = request.GET.get('range', '7days')
    intent_filter = request.GET.get('intent', '')

    now = timezone.now()
    if time_range == 'today':
        start_date = now.replace(hour=0, minute=0, second=0)
    elif time_range == '7days':
        start_date = now - timedelta(days=7)
    elif time_range == '30days':
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=90)

    logs = AIConversationLog.objects.filter(created_at__gte=start_date)
    if intent_filter:
        logs = logs.filter(intent_detected=intent_filter)

    total_conversations = logs.values('session_id').distinct().count()
    total_messages = logs.count()
    avg_accuracy = logs.aggregate(avg=Avg('confidence_score'))['avg'] or 0
    escalation_rate = (logs.filter(was_escalated=True).count() / max(total_messages, 1)) * 100

    intent_counts = logs.values('intent_detected').annotate(count=Count('intent')).order_by('-count')[:8]
    total_intent_count = sum(item['count'] for item in intent_counts)

    daily_stats = logs.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(count=Count('id')).order_by('date')

    labels = [item['date'].strftime('%d/%m') if item['date'] else '' for item in daily_stats]
    data = [item['count'] for item in daily_stats]

    intent_labels = [dict(INTENT_CHOICES).get(item['intent_detected'] or 'unknown', item['intent_detected'] or 'Khác') for item in intent_counts]
    intent_data = [item['count'] for item in intent_counts]

    recent_logs = logs.select_related().order_by('-created_at')[:10]
    recent_conversations = []
    for log in recent_logs:
        try:
            session = ChatSession.objects.get(session_id=log.session_id)
            user_name = session.account.full_name if session.account else 'Khách'
        except ChatSession.DoesNotExist:
            user_name = 'Khách'
        recent_conversations.append({
            'session_id': str(log.session_id),
            'user_name': user_name,
            'user_initial': user_name[0].upper() if user_name else 'U',
            'last_message': log.user_message,
            'intent': log.intent_detected,
            'created_at': log.created_at,
        })

    context = {
        'page_title': 'Dashboard Chat AI',
        'active_menu': 'chat',
        'stats': {
            'total_conversations': total_conversations,
            'total_messages': total_messages,
            'avg_intent_accuracy': round(float(avg_accuracy) * 100, 1) if avg_accuracy else 0,
            'escalation_rate': round(escalation_rate, 1),
            'avg_response_time': '1.2',
            'avg_rating': '4.8',
        },
        'chart_labels': labels,
        'chart_data': data,
        'intent_labels': intent_labels,
        'intent_data': intent_data,
        'response_time_data': data,
        'top_products': [],
        'recent_conversations': recent_conversations,
        'time_range': time_range,
        'intent_filter': intent_filter,
    }
    return render(request, 'chat/admin_dashboard.html', context)


@admin_required
def chat_list(request):
    """Trang danh sách phiên chat."""
    sessions = ChatSession.objects.select_related('account', 'assigned_to').all().order_by('-started_at')

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        sessions = sessions.filter(status=status_filter)

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        sessions = sessions.filter(
            Q(session_id__icontains=search_query) |
            Q(account__username__icontains=search_query) |
            Q(account__full_name__icontains=search_query)
        )

    # Paginate
    page_obj, paginator = paginate_queryset(request, sessions, 20)

    # Status counts
    status_counts = ChatSession.objects.values('status').annotate(count=Count('status'))
    status_dict = {item['status'].lower(): item['count'] for item in status_counts}
    total_chats = sum(status_dict.values())

    context = {
        'page_title': 'Quản lý chat',
        'active_menu': 'chat',
        'sessions': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_counts': status_dict,
        'total_chats': total_chats,
        'waiting': status_dict.get('waiting', 0),
    }
    return render(request, 'chat/chat_list.html', context)


@admin_required
def chat_detail(request, session_id):
    """Chi tiết phiên chat."""
    session = get_object_or_404(ChatSession.objects.prefetch_related('messages', 'messages__sender'), session_id=session_id)
    messages_list = session.messages.all().order_by('created_at')

    # Get employees for assignment
    employees = Account.objects.filter(role__in=['Admin', 'Employee'], is_active=True)

    context = {
        'page_title': f'Chat - {session.account.username if session.account else "Khách"}',
        'active_menu': 'chat',
        'session': session,
        'messages': messages_list,
        'employees': employees,
    }
    return render(request, 'chat/chat_detail.html', context)


@admin_required
def chat_send_message(request, session_id):
    """Gửi tin nhắn trong phiên chat (AJAX)."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'})

    session = get_object_or_404(ChatSession, session_id=session_id)
    message_text = request.POST.get('message', '').strip()

    if not message_text:
        return JsonResponse({'success': False, 'message': 'Tin nhắn trống!'})

    # Create message
    chat_message = ChatMessage.objects.create(
        session=session,
        message=message_text,
        sender_type='admin',
        sender=request.user
    )

    # Update session status
    if session.status == 'Waiting':
        session.status = 'Active'
        session.assigned_to = request.user
        session.save()

    return JsonResponse({
        'success': True,
        'message': 'Đã gửi tin nhắn!',
        'data': {
            'id': chat_message.message_id,
            'message': chat_message.message,
            'sender': request.user.username,
            'created_at': chat_message.created_at.strftime('%H:%i'),
            'sender_type': 'admin'
        }
    })


@admin_required
def chat_assign(request, session_id):
    """Gán phiên chat cho nhân viên."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'})

    session = get_object_or_404(ChatSession, session_id=session_id)
    employee_id = request.POST.get('employee_id')

    if employee_id:
        employee = get_object_or_404(Account, pk=employee_id, role__in=['Admin', 'Employee'])
        session.assigned_to = employee
        session.save()

    return JsonResponse({'success': True, 'message': 'Đã gán phiên chat!'})


@admin_required
def chat_close(request, session_id):
    """Đóng phiên chat."""
    session = get_object_or_404(ChatSession, session_id=session_id)
    session.status = 'Closed'
    session.ended_at = timezone.now()
    session.save()

    messages.success(request, 'Đã đóng phiên chat!')
    return redirect('chat:chat_list')


@admin_required
def ai_logs(request):
    """Trang log AI conversation."""
    logs = AIConversationLog.objects.all().order_by('-created_at')

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        logs = logs.filter(
            Q(user_message__icontains=search_query) |
            Q(ai_response__icontains=search_query) |
            Q(intent_detected__icontains=search_query)
        )

    # Paginate
    page_obj, paginator = paginate_queryset(request, logs, 30)

    context = {
        'page_title': 'Log AI Conversation',
        'active_menu': 'chat',
        'logs': page_obj,
        'paginator': paginator,
        'search_query': search_query,
    }
    return render(request, 'chat/ai_logs.html', context)


@admin_required
def ai_status(request):
    """Trang xem trạng thái các AI providers."""
    from apps.chat.services.ai_service import ai_service

    status = ai_service.get_status()

    context = {
        'page_title': 'AI Status',
        'active_menu': 'chat',
        'provider_status': status,
    }
    return render(request, 'chat/ai_status.html', context)


@admin_required
def chat_start(request):
    """Tạo phiên chat mới (admin tạo cho khách)."""
    if request.method == 'POST':
        session = ChatSession.objects.create(
            status='Waiting'
        )
        return redirect('chat:chat_detail', session_id=session.session_id)

    return redirect('chat:chat_list')


# =====================
# Public API Endpoints (for chatbot integration)
# These endpoints are intentionally public for customer-facing chatbot
# =====================

@require_http_methods(["POST"])
def api_send_message(request):
    """API gửi tin nhắn chatbot - kết hợp Gemini + Rule-based."""
    try:
        message = request.POST.get('message', '').strip()
        if not message:
            return JsonResponse({'success': False, 'error': 'Tin nhắn trống'}, status=400)

        # Tạo hoặc lấy session
        session_id_str = request.POST.get('session_id', '').strip()
        if session_id_str:
            try:
                session = ChatSession.objects.get(session_id=session_id_str)
            except (ChatSession.DoesNotExist, ValueError):
                session = ChatSession.objects.create(status='Waiting')
        else:
            session = ChatSession.objects.create(status='Waiting')

        # Lưu tin nhắn user
        ChatMessage.objects.create(
            session=session,
            message=message,
            sender_type='user'
        )

        # Gọi AI service
        response_text, intent, products, should_escalate = ai_service.generate_response(message)

        # Log AI conversation
        AIConversationLog.objects.create(
            session_id=session.session_id,
            user_message=message,
            ai_response=response_text,
            intent_detected=intent,
            was_escalated=should_escalate
        )

        # Lưu phản hồi AI
        ChatMessage.objects.create(
            session=session,
            message=response_text,
            sender_type='bot',
            metadata={'intent': intent, 'products_count': len(products)}
        )

        return JsonResponse({
            'success': True,
            'session_id': str(session.session_id),
            'message': response_text,
            'intent': intent,
            'products': products,
            'should_escalate': should_escalate
        })

    except Exception as e:
        logger.error(f"API send message error: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# Public API - chatbot integration
@require_http_methods(["GET"])
def api_get_history(request, session_id):
    """API lấy lịch sử chat."""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages_qs = session.messages.all().order_by('created_at')

        messages_data = [
            {
                'message_id': msg.message_id,
                'message': msg.message,
                'sender_type': msg.sender_type,
                'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for msg in messages_qs
        ]

        return JsonResponse({'success': True, 'messages': messages_data})

    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
    except Exception as e:
        logger.error(f"API history error: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["GET"])
def api_new_messages(request, session_id):
    """API lấy tin nhắn mới (polling)."""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        last_id = int(request.GET.get('last_id', 0))

        new_messages = session.messages.filter(
            message_id__gt=last_id,
            sender_type__in=['admin', 'bot']
        ).order_by('created_at')

        messages_data = [
            {
                'message_id': msg.message_id,
                'message': msg.message,
                'sender_type': msg.sender_type,
                'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for msg in new_messages
        ]

        return JsonResponse({'success': True, 'messages': messages_data})

    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
    except Exception as e:
        logger.error(f"API new messages error: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
def api_escalate(request):
    """API chuyển chat sang nhân viên."""
    try:
        session_id = request.POST.get('session_id', '').strip()
        if not session_id:
            return JsonResponse({'success': False, 'error': 'Session ID required'}, status=400)

        session = ChatSession.objects.get(session_id=session_id)
        session.status = 'Waiting'
        session.save()

        return JsonResponse({'success': True, 'message': 'Đã chuyển yêu cầu đến nhân viên'})

    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
    except Exception as e:
        logger.error(f"API escalate error: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
