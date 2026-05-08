"""
Views cho app faqs.
CRUD cho FAQ model.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset
from .models import FAQ
from .forms import FAQForm


# =====================
# Public Views (Shop)
# =====================

def support(request):
    """Trang hỗ trợ khách hàng - công khai."""
    faqs = FAQ.objects.filter(is_active=True).order_by('priority', '-created_at')
    
    # Lọc theo danh mục
    category = request.GET.get('category')
    if category:
        faqs = faqs.filter(category=category)
    
    # Tìm kiếm
    query = request.GET.get('q', '').strip()
    if query:
        faqs = faqs.filter(
            Q(question__icontains=query) |
            Q(answer__icontains=query)
        )
    
    # Nhóm FAQ theo category
    faq_categories = {}
    for faq in faqs:
        cat = faq.category or 'Khác'
        if cat not in faq_categories:
            faq_categories[cat] = []
        faq_categories[cat].append(faq)
    
    # Lấy danh sách categories cho filter
    all_categories = list(set(faq.category or 'Khác' for faq in FAQ.objects.filter(is_active=True)))
    
    context = {
        'faqs': faqs,
        'faq_categories': faq_categories,
        'all_categories': sorted(all_categories),
        'selected_category': category,
        'search_query': query,
    }
    return render(request, 'shop/support.html', context)


# =====================
# Admin Views
# =====================

@admin_required
def faq_list(request):
    """Trang danh sách FAQ."""
    faqs = FAQ.objects.all().order_by('-priority', '-created_at')

    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        faqs = faqs.filter(category=category_filter)

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        faqs = faqs.filter(is_active=True)
    elif status_filter == 'inactive':
        faqs = faqs.filter(is_active=False)

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        faqs = faqs.filter(
            Q(question__icontains=search_query) |
            Q(answer__icontains=search_query) |
            Q(keywords__icontains=search_query)
        )

    # Paginate
    page_obj, paginator = paginate_queryset(request, faqs, 5)

    context = {
        'page_title': 'Quản lý FAQs',
        'active_menu': 'faqs',
        'faqs': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'category_filter': category_filter,
        'status_filter': status_filter,
    }
    return render(request, 'faqs/faq_list.html', context)


@admin_required
def faq_create(request):
    """Tạo FAQ mới."""
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tạo FAQ thành công!')
            return redirect('faqs:faq_list')
    else:
        form = FAQForm()

    context = {
        'page_title': 'Thêm FAQ mới',
        'active_menu': 'faqs',
        'form': form,
        'is_edit': False,
    }
    return render(request, 'faqs/faq_form.html', context)


@admin_required
def faq_update(request, pk):
    """Cập nhật FAQ."""
    faq = get_object_or_404(FAQ, pk=pk)

    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật FAQ thành công!')
            return redirect('faqs:faq_list')
    else:
        form = FAQForm(instance=faq)

    context = {
        'page_title': 'Sửa FAQ',
        'active_menu': 'faqs',
        'form': form,
        'faq': faq,
        'is_edit': True,
    }
    return render(request, 'faqs/faq_form.html', context)


@admin_required
@require_http_methods(['POST'])
def faq_delete(request, pk):
    """Xóa FAQ."""
    faq = get_object_or_404(FAQ, pk=pk)
    question = faq.question
    faq.delete()
    messages.success(request, f'Xóa FAQ "{question[:50]}..." thành công!')
    return JsonResponse({'success': True})


@admin_required
@require_http_methods(['POST'])
def faq_toggle_status(request, pk):
    """Toggle trạng thái FAQ."""
    faq = get_object_or_404(FAQ, pk=pk)
    faq.is_active = not faq.is_active
    faq.save()

    status_text = 'Kích hoạt' if faq.is_active else 'Vô hiệu hóa'
    return JsonResponse({
        'success': True,
        'message': f'{status_text} FAQ thành công!',
        'is_active': faq.is_active
    })
