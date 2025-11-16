from django.contrib import admin
from django.contrib.admin import actions
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_quantity', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    actions = [actions.delete_selected, 'confirm_orders', 'cancel_orders']
    
    class Media:
        js = ('admin/js/order_admin.js',)
    
    def get_fields(self, request, obj=None):
        """Показываем поле причины отмены только при редактировании отмененного заказа"""
        fields = ['user', 'status', 'created_at', 'updated_at']
        if obj and obj.status == 'cancelled':
            fields.insert(2, 'cancellation_reason')
        return fields
    
    def total_quantity(self, obj):
        return obj.total_quantity
    total_quantity.short_description = 'Количество товаров'
    
    def total_price(self, obj):
        return f"{obj.total_price:.2f} руб."
    total_price.short_description = 'Общая стоимость'
    
    def confirm_orders(self, request, queryset):
        """Подтвердить выбранные заказы"""
        updated = queryset.filter(status='new').update(status='confirmed')
        self.message_user(request, f'Подтверждено {updated} заказов.')
    confirm_orders.short_description = "Подтвердить выбранные заказы"
    confirm_orders.allowed_permissions = ('change',)
    
    def cancel_orders(self, request, queryset):
        """Отменить выбранные заказы с указанием причины"""
        # Проверяем, был ли отправлен POST с причиной отмены
        if request.POST.get('apply'):
            # Восстанавливаем queryset из _selected_action, если queryset пустой
            # (это происходит когда форма отправляется обратно в admin)
            if not queryset.exists():
                order_ids = request.POST.getlist('_selected_action')
                if order_ids:
                    queryset = Order.objects.filter(id__in=order_ids)
            
            reason = request.POST.get('cancellation_reason', '').strip()
            if not reason:
                self.message_user(request, 'Причина отмены не может быть пустой.', level='ERROR')
                # Показываем форму снова с ошибкой
                from django.shortcuts import render
                return render(request, 'admin/orders/order/add_cancellation_reason.html', {
                    'orders': queryset,
                    'action_name': 'cancel_orders',
                })
            
            # Используем queryset для обновления заказов
            updated = queryset.filter(status__in=['new', 'confirmed']).update(
                status='cancelled',
                cancellation_reason=reason
            )
            self.message_user(request, f'Отменено {updated} заказов с указанием причины.')
            # Возвращаем None - Django автоматически сделает редирект на changelist
            return None
        else:
            # Показываем форму для ввода причины (первый запрос)
            from django.shortcuts import render
            return render(request, 'admin/orders/order/add_cancellation_reason.html', {
                'orders': queryset,
                'action_name': 'cancel_orders',
            })
    cancel_orders.short_description = "Отменить заказ"
    cancel_orders.allowed_permissions = ('change',)

