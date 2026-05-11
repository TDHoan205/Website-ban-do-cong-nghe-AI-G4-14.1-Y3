"""
Views cho app accounts.
CRUD cho Account và Employee models.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone
from django.conf import settings

from apps.core.decorators import admin_required, ajax_required
from apps.core.utils import paginate_queryset, format_currency
from .models import Account, Employee, PasswordReset
from .forms import AccountForm, EmployeeForm, LoginForm, RegisterForm, ForgotPasswordForm
from apps.cart.models import CartItem


# =====================
# Authentication Views
# =====================

def login_view(request):
    """Trang dang nhap - ho tro guest cart merge."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Merge guest cart vao member cart truoc khi login
                    if request.session.session_key:
                        _merge_guest_cart(request, user)
                    login(request, user)
                    next_url = request.GET.get('next', 'dashboard:index')
                    messages.success(request, f'Chao mung {user.username}!')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Tai khoan da bi khoa!')
            else:
                messages.error(request, 'Ten dang nhap hoac mat khau khong dung!')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def _merge_guest_cart(request, user):
    """Gop gio hang cua guest vao tai khoan khi dang nhap."""
    if request.session.session_key is None:
        return
    guest_items = CartItem.objects.filter(session_key=request.session.session_key)
    for guest_item in guest_items:
        existing = CartItem.objects.filter(
            account=user,
            product=guest_item.product,
            variant=guest_item.variant
        ).first()
        if existing:
            existing.quantity += guest_item.quantity
            max_stock = guest_item.variant.stock_quantity if guest_item.variant else guest_item.product.stock_quantity
            if existing.quantity > max_stock:
                existing.quantity = max_stock
            existing.save()
        else:
            CartItem.objects.create(
                account=user,
                product=guest_item.product,
                variant=guest_item.variant,
                quantity=guest_item.quantity
            )
        guest_item.delete()


def logout_view(request):
    """Đăng xuất."""
    logout(request)
    messages.success(request, 'Đã đăng xuất thành công!')
    return redirect('accounts:login')


def register_view(request):
    """Trang đăng ký tài khoản mới."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            account = form.save()
            messages.success(request, 'Tạo tài khoản thành công! Vui lòng đăng nhập.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def forgot_password_view(request):
    """Trang quen mat khau - gui email reset."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            account = Account.objects.get(email__iexact=email)
            # Tao token reset
            import secrets
            from django.utils import timezone
            from datetime import timedelta

            # Vo hieu hoa token cu
            PasswordReset.objects.filter(account=account, used=False).update(used=True)

            token = secrets.token_urlsafe(48)
            expires_at = timezone.now() + timedelta(hours=24)
            reset = PasswordReset.objects.create(
                account=account,
                token=token,
                expires_at=expires_at
            )

            # Gui email
            reset_url = request.build_absolute_uri(
                f'/accounts/reset-password/?token={token}&email={account.email}'
            )

            try:
                from django.core.mail import send_mail
                send_mail(
                    subject='[TechStore] Dat lai mat khau',
                    message=f'''Xin chao {account.full_name or account.username},

Ban yeu cau dat lai mat khau cho tai khoan TechStore.

Nhan vao link sau de dat lai mat khau:
{reset_url}

Link nay co hieu luc trong 24 gio.

Neu ban khong yeu cau dat lai mat khau, vui long bo qua email nay.

TechStore
''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[account.email],
                    fail_silently=True,
                )
            except Exception:
                pass  # Neu email that bai, van hien thi thong bao thanh cong

            messages.success(request, f'Da gui link dat lai mat khau den email {email}. Vui long kiem tra hop thu.')
        except Account.DoesNotExist:
            # Van hien thi thong bao thanh cong de tranh email enumeration
            messages.success(request, f'Neu email ton tai trong he thong, link dat lai mat khau da duoc gui.')

    return render(request, 'accounts/forgot_password.html')


def reset_password_view(request):
    """Trang dat lai mat khau."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    token = request.GET.get('token', '').strip()
    email = request.GET.get('email', '').strip()

    if not token or not email:
        messages.error(request, 'Link dat lai mat khau khong hop le.')
        return redirect('accounts:forgot_password')

    try:
        account = Account.objects.get(email__iexact=email)
        reset = PasswordReset.objects.filter(
            account=account,
            token=token,
            used=False,
            expires_at__gt=timezone.now()
        ).first()

        if not reset:
            messages.error(request, 'Link dat lai mat khau da het han hoac khong ton tai.')
            return redirect('accounts:forgot_password')

        if request.method == 'POST':
            password = request.POST.get('password', '').strip()
            password2 = request.POST.get('password2', '').strip()

            if len(password) < 6:
                messages.error(request, 'Mat khau phai it nhat 6 ky tu.')
            elif password != password2:
                messages.error(request, 'Mat khau xac nhan khong khop.')
            else:
                account.set_password(password)
                account.save()
                reset.used = True
                reset.save()
                messages.success(request, 'Dat lai mat khau thanh cong! Vui long dang nhap.')
                return redirect('accounts:login')

        return render(request, 'accounts/reset_password.html', {
            'token': token, 'email': email
        })

    except Account.DoesNotExist:
        messages.error(request, 'Link dat lai mat khau khong hop le.')
        return redirect('accounts:forgot_password')


# =====================
# Account Views
# =====================

@admin_required
def account_list(request):
    """Trang danh sách tài khoản."""
    accounts = Account.objects.all().select_related('employee_profile').order_by('-created_at')

    # Filter by role
    role_filter = request.GET.get('role')
    if role_filter:
        accounts = accounts.filter(role=role_filter)

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        is_active = status_filter == 'active'
        accounts = accounts.filter(is_active=is_active)

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        accounts = accounts.filter(
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(full_name__icontains=search_query) |
            models.Q(phone__icontains=search_query)
        )

    # Paginate
    page_obj, paginator = paginate_queryset(request, accounts, 5)

    # Role counts for filter tabs
    total_count = Account.objects.count()
    admin_count = Account.objects.filter(role='Admin').count()
    employee_count = Account.objects.filter(role='Employee').count()
    customer_count = Account.objects.filter(role='Customer').count()

    context = {
        'page_title': 'Quản lý tài khoản',
        'active_menu': 'accounts',
        'accounts': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'total_count': total_count,
        'admin_count': admin_count,
        'employee_count': employee_count,
        'customer_count': customer_count,
    }
    return render(request, 'accounts/account_list.html', context)


@admin_required
def account_create(request):
    """Tạo tài khoản mới."""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            messages.success(request, f'Tạo tài khoản "{account.username}" thành công!')
            return redirect('accounts:account_list')
    else:
        form = AccountForm()

    context = {
        'page_title': 'Thêm tài khoản mới',
        'active_menu': 'accounts',
        'form': form,
        'is_edit': False,
    }
    return render(request, 'accounts/account_form.html', context)


@admin_required
def account_update(request, pk):
    """Cập nhật tài khoản."""
    account = get_object_or_404(Account, pk=pk)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cập nhật tài khoản "{account.username}" thành công!')
            return redirect('accounts:account_list')
    else:
        form = AccountForm(instance=account)

    context = {
        'page_title': 'Sửa tài khoản',
        'active_menu': 'accounts',
        'form': form,
        'account': account,
        'is_edit': True,
    }
    return render(request, 'accounts/account_form.html', context)


@admin_required
@require_http_methods(['POST'])
def account_delete(request, pk):
    """Xóa tài khoản."""
    account = get_object_or_404(Account, pk=pk)

    if request.user == account:
        return JsonResponse({
            'success': False,
            'message': 'Bạn không thể xóa tài khoản của chính mình!'
        })

    username = account.username
    account.delete()
    messages.success(request, f'Xóa tài khoản "{username}" thành công!')

    return JsonResponse({'success': True, 'message': 'Xóa thành công!'})


@admin_required
@require_http_methods(['POST'])
def account_toggle_status(request, pk):
    """Toggle trạng thái tài khoản."""
    account = get_object_or_404(Account, pk=pk)

    if request.user == account:
        return JsonResponse({
            'success': False,
            'message': 'Bạn không thể thay đổi trạng thái tài khoản của chính mình!'
        })

    account.is_active = not account.is_active
    account.save()

    status_text = 'Kích hoạt' if account.is_active else 'Khóa'
    return JsonResponse({
        'success': True,
        'message': f'{status_text} tài khoản thành công!',
        'is_active': account.is_active
    })


# =====================
# Employee Views
# =====================

@admin_required
def employee_list(request):
    """Trang danh sách nhân viên - chuyển hướng về danh sách tài khoản với filter Employee."""
    from django.shortcuts import redirect
    return redirect(f"{request.path.replace('employees/', '')}?role=Employee")


@admin_required
def employee_create(request):
    """Tạo nhân viên mới - chuyển hướng đến form tài khoản với vai trò Employee."""
    from django.shortcuts import redirect
    return redirect('accounts:account_create')


@admin_required
def employee_update(request, pk):
    """Cập nhật thông tin nhân viên - chuyển hướng đến form tài khoản."""
    from django.shortcuts import redirect
    return redirect('accounts:account_update', pk=pk)


@admin_required
@require_http_methods(['POST'])
def employee_delete(request, pk):
    """Xóa nhân viên."""
    employee = get_object_or_404(Employee, pk=pk)

    username = employee.account.username
    employee.account.delete()  # CASCADE sẽ xóa luôn employee
    messages.success(request, f'Xóa nhân viên "{username}" thành công!')

    return JsonResponse({'success': True, 'message': 'Xóa thành công!'})


@admin_required
@require_http_methods(['POST'])
def employee_toggle_status(request, pk):
    """Toggle trạng thái nhân viên."""
    employee = get_object_or_404(Employee, pk=pk)

    employee.is_active = not employee.is_active
    employee.save()

    employee.account.is_active = employee.is_active
    employee.account.save()

    status_text = 'Kích hoạt' if employee.is_active else 'Khóa'
    return JsonResponse({
        'success': True,
        'message': f'{status_text} nhân viên thành công!',
        'is_active': employee.is_active
    })


# =====================
# Profile View
# =====================

@login_required
def profile(request):
    """Trang thông tin cá nhân."""
    account = request.user
    employee = getattr(account, 'employee_profile', None)

    if request.method == 'POST':
        from .forms import ProfileForm
        form = ProfileForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('accounts:profile')
    else:
        from .forms import ProfileForm
        form = ProfileForm(instance=account)

    context = {
        'page_title': 'Thông tin cá nhân',
        'active_menu': 'profile',
        'account': account,
        'employee': employee,
        'profile_form': form,
    }
    return render(request, 'accounts/profile.html', context)
