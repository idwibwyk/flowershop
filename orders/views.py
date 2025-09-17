from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Cart, Order, OrderItem
from .forms import OrderConfirmationForm, OrderStatusForm
from main.models import Product


@login_required
def cart_view(request):
    """Корзина пользователя"""
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'orders/cart.html', context)


@login_required
@require_http_methods(["POST"])
def add_to_cart(request, product_id):
    """Добавление товара в корзину"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock_quantity:
        return JsonResponse({
            'success': False, 
            'message': f'Недостаточно товара на складе. Доступно: {product.stock_quantity}'
        })
    
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        if cart_item.quantity + quantity > product.stock_quantity:
            return JsonResponse({
                'success': False,
                'message': f'Недостаточно товара на складе. Доступно: {product.stock_quantity}'
            })
        cart_item.quantity += quantity
        cart_item.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Товар добавлен в корзину'
    })


@login_required
@require_http_methods(["POST"])
def update_cart_item(request, cart_item_id):
    """Обновление количества товара в корзине"""
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        return JsonResponse({'success': True, 'message': 'Товар удален из корзины'})
    
    if quantity > cart_item.product.stock_quantity:
        return JsonResponse({
            'success': False,
            'message': f'Недостаточно товара на складе. Доступно: {cart_item.product.stock_quantity}'
        })
    
    cart_item.quantity = quantity
    cart_item.save()
    
    return JsonResponse({'success': True, 'message': 'Количество обновлено'})


@login_required
@require_http_methods(["POST"])
def remove_from_cart(request, cart_item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return JsonResponse({'success': True, 'message': 'Товар удален из корзины'})


@login_required
def checkout(request):
    """Оформление заказа"""
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, 'Корзина пуста')
        return redirect('cart')
    
    if request.method == 'POST':
        form = OrderConfirmationForm(request.user, request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Создаем заказ
                order = Order.objects.create(user=request.user)
                
                # Добавляем товары в заказ
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                    
                    # Уменьшаем количество на складе
                    cart_item.product.stock_quantity -= cart_item.quantity
                    cart_item.product.save()
                
                # Очищаем корзину
                cart_items.delete()
                
                messages.success(request, 'Заказ успешно оформлен!')
                return redirect('profile')
    else:
        form = OrderConfirmationForm(request.user)
    
    total_price = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
@require_http_methods(["POST"])
def cancel_order(request, order_id):
    """Отмена заказа пользователем"""
    order = get_object_or_404(Order, id=order_id, user=request.user, status='new')
    
    with transaction.atomic():
        # Возвращаем товары на склад
        for item in order.orderitem_set.all():
            item.product.stock_quantity += item.quantity
            item.product.save()
        
        # Отменяем заказ
        order.status = 'cancelled'
        order.cancellation_reason = 'Отменен пользователем'
        order.save()
    
    messages.success(request, 'Заказ отменен')
    return redirect('profile')