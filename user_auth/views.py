from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import RegistrationForm, LoginForm


def register_view(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return JsonResponse({'success': True, 'message': 'Регистрация прошла успешно!'})
        else:
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = field_errors[0]
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = RegistrationForm()
    
    return render(request, 'user_auth/register.html', {'form': form})


def login_view(request):
    """Авторизация пользователя"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно авторизованы!')
            return JsonResponse({'success': True, 'message': 'Вы успешно авторизованы!'})
        else:
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = field_errors[0]
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = LoginForm()
    
    return render(request, 'user_auth/login.html', {'form': form})


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('home')


@login_required
def profile(request):
    """Личный кабинет пользователя"""
    from orders.models import Order
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'user_auth/profile.html', context)