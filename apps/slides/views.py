"""
Views cho app slides.
CRUD cho Slide model.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.core.decorators import admin_required
from apps.core.utils import paginate_queryset
from .models import Slide
from .forms import SlideForm


@admin_required
def slide_list(request):
    """Trang danh sách slides."""
    slides = Slide.objects.all().order_by('display_order')

    page_obj, paginator = paginate_queryset(request, slides, 20)

    context = {
        'page_title': 'Quản lý Slides',
        'active_menu': 'slides',
        'slides': page_obj,
        'paginator': paginator,
    }
    return render(request, 'slides/slide_list.html', context)


@admin_required
def slide_create(request):
    """Tạo slide mới."""
    if request.method == 'POST':
        form = SlideForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tạo slide thành công!')
            return redirect('slides:slide_list')
    else:
        form = SlideForm()

    context = {
        'page_title': 'Thêm slide mới',
        'active_menu': 'slides',
        'form': form,
        'is_edit': False,
    }
    return render(request, 'slides/slide_form.html', context)


@admin_required
def slide_update(request, pk):
    """Cập nhật slide."""
    slide = get_object_or_404(Slide, pk=pk)

    if request.method == 'POST':
        form = SlideForm(request.POST, instance=slide)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật slide thành công!')
            return redirect('slides:slide_list')
    else:
        form = SlideForm(instance=slide)

    context = {
        'page_title': 'Sửa slide',
        'active_menu': 'slides',
        'form': form,
        'slide': slide,
        'is_edit': True,
    }
    return render(request, 'slides/slide_form.html', context)


@admin_required
@require_http_methods(['POST'])
def slide_delete(request, pk):
    """Xóa slide."""
    slide = get_object_or_404(Slide, pk=pk)
    title = slide.title
    slide.delete()
    messages.success(request, f'Xóa slide "{title}" thành công!')
    return JsonResponse({'success': True, 'message': 'Xóa thành công!'})


@admin_required
@require_http_methods(['POST'])
def slide_toggle_status(request, pk):
    """Toggle trạng thái slide."""
    slide = get_object_or_404(Slide, pk=pk)
    slide.is_active = not slide.is_active
    slide.save()
    status_text = 'Hiển thị' if slide.is_active else 'Ẩn'
    return JsonResponse({
        'success': True,
        'message': f'{status_text} slide thành công!',
        'is_active': slide.is_active
    })
