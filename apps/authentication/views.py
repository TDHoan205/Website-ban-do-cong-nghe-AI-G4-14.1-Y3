"""
Views cho app authentication.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    """Trang đăng nhập."""
    from apps.users.models import Account
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:index')
        
        return render(request, 'accounts/login.html', {'error': 'Tên đăng nhập hoặc mật khẩu không đúng'})

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """Đăng xuất."""
    logout(request)
    return redirect('accounts:login')
