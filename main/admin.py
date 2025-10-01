from django.contrib import admin
from .models import Category, Product


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