"""
Views cho app reviews.
Quản lý đánh giá sản phẩm.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg
from django.shortcuts import redirect

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset
from .models import Review
from .forms import ReviewForm


@admin_required
def review_list(request):
    """Trang danh sách đánh giá."""
    reviews = Review.objects.select_related('product', 'account').all().order_by('-created_at')

    search_query = request.GET.get('q', '')
    if search_query:
        reviews = reviews.filter(
            Q(product__name__icontains=search_query) |
            Q(account__username__icontains=search_query) |
            Q(comment__icontains=search_query)
        )

    rating_filter = request.GET.get('rating')
    if rating_filter:
        reviews = reviews.filter(rating=int(rating_filter))

    approval_filter = request.GET.get('approved')
    if approval_filter == 'approved':
        reviews = reviews.filter(is_approved=True)
    elif approval_filter == 'pending':
        reviews = reviews.filter(is_approved=False)

    page_obj, paginator = paginate_queryset(request, reviews, 20)

    pending_count = Review.objects.filter(is_approved=False).count()
    avg_rating = Review.objects.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg'] or 0

    context = {
        'page_title': 'Quản lý đánh giá',
        'active_menu': 'reviews',
        'reviews': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'rating_filter': rating_filter,
        'approval_filter': approval_filter,
        'pending_count': pending_count,
        'avg_rating': avg_rating,
    }
    return render(request, 'reviews/review_list.html', context)


@admin_required
def review_update(request, pk):
    """Cập nhật đánh giá."""
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật đánh giá thành công!')
            return redirect('reviews:review_list')
    else:
        form = ReviewForm(instance=review)

    context = {
        'page_title': 'Sửa đánh giá',
        'active_menu': 'reviews',
        'form': form,
        'review': review,
        'is_edit': True,
    }
    return render(request, 'reviews/review_form.html', context)


@admin_required
@require_http_methods(['POST'])
def review_toggle_approval(request, pk):
    """Toggle trạng thái duyệt đánh giá."""
    review = get_object_or_404(Review, pk=pk)
    review.is_approved = not review.is_approved
    review.save()
    status_text = 'Duyệt' if review.is_approved else 'Bỏ duyệt'
    return JsonResponse({
        'success': True,
        'message': f'{status_text} đánh giá thành công!',
        'is_approved': review.is_approved
    })


@admin_required
@require_http_methods(['POST'])
def review_delete(request, pk):
    """Xóa đánh giá."""
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    messages.success(request, 'Xóa đánh giá thành công!')
    return JsonResponse({'success': True, 'message': 'Xóa thành công!'})


@admin_required
@require_http_methods(['POST'])
def review_approve_all(request):
    """Duyệt tất cả đánh giá chưa duyệt."""
    count = Review.objects.filter(is_approved=False).update(is_approved=True)
    messages.success(request, f'Đã duyệt {count} đánh giá!')
    return JsonResponse({'success': True, 'message': f'Đã duyệt {count} đánh giá!'})
