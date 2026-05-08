"""
Core mixins cho class-based views.
Chứa các Mixin dùng chung cho tất cả views.
"""
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages


class AdminRequiredMixin:
    """
    Mixin yêu cầu đăng nhập với quyền Admin hoặc Employee.
    Sử dụng: class MyView(AdminRequiredMixin, ListView):
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not (request.user.is_staff or getattr(request.user, 'role', None) in ['Admin', 'Employee']):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AdminOnlyMixin:
    """
    Mixin yêu cầu đăng nhập với quyền Admin only.
    Sử dụng: class MyView(AdminOnlyMixin, DeleteView):
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        role = getattr(request.user, 'role', None)
        if role != 'Admin' and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CustomerRequiredMixin:
    """
    Mixin yêu cầu đăng nhập với quyền Customer.
    Sử dụng: class MyView(CustomerRequiredMixin, View):
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        role = getattr(request.user, 'role', None)
        if role not in ['Customer', 'Admin', 'Employee']:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class SuperUserMixin:
    """
    Mixin yêu cầu Super User.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class BaseMixin:
    """
    Mixin cơ bản với các thuộc tính và phương thức dùng chung.
    """
    page_title = ''
    page_subtitle = ''
    active_menu = ''
    breadcrumbs = []

    def get_page_title(self):
        return self.page_title

    def get_page_subtitle(self):
        return self.page_subtitle

    def get_active_menu(self):
        return self.active_menu

    def get_breadcrumbs(self):
        return self.breadcrumbs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        context['page_subtitle'] = self.get_page_subtitle()
        context['active_menu'] = self.get_active_menu()
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class AdminMixin(BaseMixin, AdminRequiredMixin):
    """
    Mixin kết hợp BaseMixin và AdminRequiredMixin cho admin pages.
    """
    pass


class FormValidMixin:
    """
    Mixin xử lý form validation messages.
    """
    def form_valid(self, form):
        messages.success(self.request, 'Lưu thành công!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.')
        return super().form_invalid(form)


class DeleteSuccessMessageMixin:
    """
    Mixin hiển thị thông báo khi xóa thành công.
    """
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Xóa thành công!')
        return super().delete(request, *args, **kwargs)


class AjaxResponseMixin:
    """
    Mixin xử lý AJAX response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        from django.http import JsonResponse
        return JsonResponse(context, **response_kwargs)

    def form_valid(self, form):
        from django.http import JsonResponse
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Lưu thành công!',
                'data': {'id': form.instance.pk}
            })
        return response

    def form_invalid(self, form):
        from django.http import JsonResponse
        response = super().form_invalid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Có lỗi xảy ra!',
                'errors': form.errors
            }, status=400)
        return response


class SearchMixin:
    """
    Mixin hỗ trợ tìm kiếm trong queryset.
    """
    search_fields = []
    search_placeholder = 'Tìm kiếm...'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query and self.search_fields:
            from django.db.models import Q
            q_filter = Q()
            for field in self.search_fields:
                q_filter |= Q(**{f'{field}__icontains': search_query})
            queryset = queryset.filter(q_filter)
        return queryset

    def get_search_query(self):
        return self.request.GET.get('q', '')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.get_search_query()
        context['search_placeholder'] = self.search_placeholder
        return context


class FilterMixin:
    """
    Mixin hỗ trợ lọc queryset.
    """
    filter_fields = {}

    def get_queryset(self):
        queryset = super().get_queryset()
        for param, field in self.filter_fields.items():
            value = self.request.GET.get(param)
            if value:
                queryset = queryset.filter(**{field: value})
        return queryset

    def get_filter_context(self):
        return {param: self.request.GET.get(param, '')
                for param in self.filter_fields.keys()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = self.get_filter_context()
        return context
