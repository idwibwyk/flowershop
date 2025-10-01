from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    actions = ['delete_selected_categories']
    
    def delete_selected_categories(self, request, queryset):
        """Удалить выбранные категории"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Удалено {count} категорий.')
    delete_selected_categories.short_description = "Удалить выбранные категории"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'model', 'country']
    ordering = ['-created_at']
    list_editable = ['price', 'stock_quantity', 'is_available']
    actions = ['delete_selected_products']
    
    def save_model(self, request, obj, form, change):
        # Валидация цены - не может быть отрицательной
        if obj.price < 0:
            from django.core.exceptions import ValidationError
            raise ValidationError("Цена не может быть отрицательной")
        super().save_model(request, obj, form, change)
    
    def delete_selected_products(self, request, queryset):
        """Удалить выбранные товары"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Удалено {count} товаров.')
    delete_selected_products.short_description = "Удалить выбранные товары"