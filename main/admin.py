from django.contrib import admin
from .models import Category, Product, SliderImage, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'model', 'country']
    ordering = ['-created_at']
    list_editable = ['price', 'stock_quantity', 'is_available']
    
    def save_model(self, request, obj, form, change):
        # Валидация цены - не может быть отрицательной
        if obj.price < 0:
            from django.core.exceptions import ValidationError
            raise ValidationError("Цена не может быть отрицательной")
        super().save_model(request, obj, form, change)


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_filter = ['is_active']
    ordering = ['order']
    list_editable = ['is_active', 'order']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'email']