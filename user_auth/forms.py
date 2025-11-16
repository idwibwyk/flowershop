from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=6,
        label='Пароль',
        help_text='Минимум 6 символов'
    )
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Повторите пароль'
    )
    rules = forms.BooleanField(
        required=True,
        label='Согласие с правилами регистрации',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество (необязательно)'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'username': 'Логин',
            'email': 'Email',
        }
    
    def clean_first_name(self):
        """Валидация имени"""
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', first_name):
            raise ValidationError('Разрешены только кириллица, пробел и тире')
        return first_name
    
    def clean_last_name(self):
        """Валидация фамилии"""
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', last_name):
            raise ValidationError('Разрешены только кириллица, пробел и тире')
        return last_name
    
    def clean_patronymic(self):
        """Валидация отчества"""
        patronymic = self.cleaned_data.get('patronymic')
        if patronymic and not re.match(r'^[а-яА-ЯёЁ\s\-]+$', patronymic):
            raise ValidationError('Разрешены только кириллица, пробел и тире')
        return patronymic
    
    def clean_username(self):
        """Валидация логина"""
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9\-]+$', username):
            raise ValidationError('Разрешены только латиница, цифры и тире')
        return username
    
    def clean_password_repeat(self):
        """Проверка совпадения паролей"""
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password and password_repeat and password != password_repeat:
            raise ValidationError('Пароли не совпадают')
        return password_repeat
    
    def save(self, commit=True):
        """Сохранение пользователя с хешированием пароля"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Форма авторизации пользователя"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
        label='Логин'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Пароль'
    )
    
    class Meta:
        fields = ['username', 'password']
    
    def clean(self):
        """Кастомная валидация формы авторизации"""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Проверяем существование пользователя
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise ValidationError('Пользователь с таким логином не найден')
            
            # Проверяем пароль
            if not user.check_password(password):
                raise ValidationError('Неверный пароль')
            
            # Проверяем активность пользователя
            if not user.is_active:
                raise ValidationError('Аккаунт заблокирован')
            
            # Устанавливаем пользователя для AuthenticationForm
            self.user_cache = user
        
        return self.cleaned_data
    
    def get_user(self):
        """Возвращает аутентифицированного пользователя"""
        return getattr(self, 'user_cache', None)

