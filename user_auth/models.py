from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """Расширенная модель пользователя"""
    name_validator = RegexValidator(
        regex=r'^[а-яА-ЯёЁ\s\-]+$',
        message='Разрешены только кириллица, пробел и тире'
    )
    login_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9\-]+$',
        message='Разрешены только латиница, цифры и тире'
    )
    
    first_name = models.CharField(
        max_length=150, 
        validators=[name_validator],
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150, 
        validators=[name_validator],
        verbose_name='Фамилия'
    )
    patronymic = models.CharField(
        max_length=150, 
        blank=True,
        validators=[name_validator],
        verbose_name='Отчество'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[login_validator],
        verbose_name='Логин'
    )
    email = models.EmailField(unique=True, verbose_name='Email')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def get_full_name(self):
        """Полное имя пользователя"""
        full_name = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name.strip()
    
    def __str__(self):
        return self.get_full_name() or self.username