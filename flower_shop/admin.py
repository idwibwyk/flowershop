"""
Кастомная админ-панель для проекта Flowlow
Настройка стандартной админ-панели Django
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Кастомизируем стандартную админ-панель Django
admin.site.site_header = _('Административная панель Flowlow')
admin.site.site_title = _('Flowlow Admin')
admin.site.index_title = _('Добро пожаловать в панель управления')

