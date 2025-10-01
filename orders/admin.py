from django.contrib import admin
from .models import Order, OrderItem, Cart


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_quantity', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    actions = ['confirm_orders', 'cancel_orders']
    fields = ['user', 'status', 'cancellation_reason', 'created_at', 'updated_at']
    
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
    
    def cancel_orders(self, request, queryset):
        """Отменить выбранные заказы"""
        updated = queryset.filter(status__in=['new', 'confirmed']).update(status='cancelled')
        self.message_user(request, f'Отменено {updated} заказов.')
    cancel_orders.short_description = "Отменить выбранные заказы"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total_price']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['product__name', 'order__user__username']
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():.2f} руб."
    get_total_price.short_description = 'Общая стоимость'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'get_total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():.2f} руб."
    get_total_price.short_description = 'Общая стоимость'