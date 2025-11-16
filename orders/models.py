from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Product

User = get_user_model()


class Order(models.Model):
    """Модель заказа"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('cancelled', 'Отменен'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    cancellation_reason = models.TextField(blank=True, verbose_name='Причина отмены')
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.user.get_full_name()}"
    
    @property
    def total_quantity(self):
        """Общее количество товаров в заказе"""
        return sum(item.quantity for item in self.orderitem_set.all())
    
    @property
    def total_price(self):
        """Общая стоимость заказа"""
        return sum(item.get_total_price() for item in self.orderitem_set.all())


class OrderItem(models.Model):
    """Модель элемента заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт."
    
    def save(self, *args, **kwargs):
        """Автоматически устанавливаем цену из товара, если она не указана"""
        if self.product and (self.price is None or self.price == 0):
            self.price = self.product.price
        super().save(*args, **kwargs)
    
    def get_total_price(self):
        """Общая стоимость элемента заказа"""
        return self.quantity * self.price


class Cart(models.Model):
    """Модель корзины"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
    def get_total_price(self):
        """Общая стоимость элемента корзины"""
        return self.quantity * self.product.price


@receiver(post_save, sender=Order)
def update_stock_on_order_confirmation(sender, instance, created, **kwargs):
    """Уменьшает количество товаров на складе при подтверждении заказа"""
    if not created and instance.status == 'confirmed':
        # Проверяем, не был ли заказ уже подтвержден ранее
        if Order.objects.filter(id=instance.id, status='confirmed').exists():
            # Уменьшаем количество товаров на складе
            for item in instance.orderitem_set.all():
                item.product.stock_quantity -= item.quantity
                if item.product.stock_quantity < 0:
                    item.product.stock_quantity = 0
                item.product.save()