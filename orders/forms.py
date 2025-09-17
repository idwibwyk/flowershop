from django import forms
from .models import Order


class OrderConfirmationForm(forms.Form):
    """Форма подтверждения заказа"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль для подтверждения заказа'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_password(self):
        """Проверка пароля пользователя"""
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return password


class OrderStatusForm(forms.ModelForm):
    """Форма изменения статуса заказа (для администратора)"""
    class Meta:
        model = Order
        fields = ['status', 'cancellation_reason']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'cancellation_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'status': 'Статус заказа',
            'cancellation_reason': 'Причина отмены',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Скрываем поле причины отмены, если статус не "отменен"
        if self.instance and self.instance.status != 'cancelled':
            self.fields['cancellation_reason'].widget = forms.HiddenInput()

