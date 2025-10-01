from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    country = models.CharField(max_length=100, verbose_name='Страна-производитель')
    year = models.IntegerField(verbose_name='Год выпуска', validators=[MinValueValidator(1900)])
    model = models.CharField(max_length=100, verbose_name='Модель')
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def clean(self):
        """Валидация модели"""
        if self.price < 0:
            raise ValidationError({'price': 'Цена не может быть отрицательной'})
        if self.stock_quantity < 0:
            raise ValidationError({'stock_quantity': 'Количество на складе не может быть отрицательным'})
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class SliderImage(models.Model):
    """Модель для слайдера на главной странице"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='slider/', verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    
    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Contact(models.Model):
    """Модель контактной информации"""
    address = models.CharField(max_length=300, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    map_image = models.ImageField(upload_to='contacts/', blank=True, verbose_name='Карта')
    
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
    
    def __str__(self):
        return f"Контакты - {self.address}"