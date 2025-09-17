from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import Category, Product, SliderImage, Contact
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем заполнение базы данных...')
        
        # Создаем суперпользователя
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Администратор',
                last_name='Системы'
            )
            self.stdout.write('Создан суперпользователь: admin/admin123')
        
        # Создаем категории
        categories_data = [
            {'name': 'Розы', 'description': 'Классические розы различных сортов и цветов'},
            {'name': 'Тюльпаны', 'description': 'Яркие весенние тюльпаны'},
            {'name': 'Лилии', 'description': 'Элегантные лилии с нежным ароматом'},
            {'name': 'Хризантемы', 'description': 'Осенние хризантемы различных оттенков'},
            {'name': 'Герберы', 'description': 'Яркие и жизнерадостные герберы'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Создана категория: {category.name}')
        
        # Создаем товары
        products_data = [
            {
                'name': 'Букет красных роз',
                'description': 'Классический букет из 25 красных роз с зеленью',
                'price': Decimal('2500.00'),
                'category': 'Розы',
                'country': 'Эквадор',
                'year': 2024,
                'model': 'Rosa Red Classic',
                'stock_quantity': 10
            },
            {
                'name': 'Букет белых роз',
                'description': 'Элегантный букет из 15 белых роз',
                'price': Decimal('1800.00'),
                'category': 'Розы',
                'country': 'Эквадор',
                'year': 2024,
                'model': 'Rosa White Elegant',
                'stock_quantity': 8
            },
            {
                'name': 'Тюльпаны разноцветные',
                'description': 'Яркий букет из разноцветных тюльпанов',
                'price': Decimal('1200.00'),
                'category': 'Тюльпаны',
                'country': 'Нидерланды',
                'year': 2024,
                'model': 'Tulip Mixed Colors',
                'stock_quantity': 15
            },
            {
                'name': 'Лилии белые',
                'description': 'Нежные белые лилии с зеленью',
                'price': Decimal('2200.00'),
                'category': 'Лилии',
                'country': 'Россия',
                'year': 2024,
                'model': 'Lily White Pure',
                'stock_quantity': 6
            },
            {
                'name': 'Хризантемы осенние',
                'description': 'Теплые осенние хризантемы в оранжевых тонах',
                'price': Decimal('1500.00'),
                'category': 'Хризантемы',
                'country': 'Россия',
                'year': 2024,
                'model': 'Chrysanthemum Autumn',
                'stock_quantity': 12
            },
            {
                'name': 'Герберы радужные',
                'description': 'Яркие герберы всех цветов радуги',
                'price': Decimal('1800.00'),
                'category': 'Герберы',
                'country': 'Колумбия',
                'year': 2024,
                'model': 'Gerbera Rainbow',
                'stock_quantity': 9
            },
        ]
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'category': categories[prod_data['category']],
                    'country': prod_data['country'],
                    'year': prod_data['year'],
                    'model': prod_data['model'],
                    'stock_quantity': prod_data['stock_quantity'],
                    'is_available': True
                }
            )
            if created:
                self.stdout.write(f'Создан товар: {product.name}')
        
        # Создаем слайды для главной страницы
        slider_data = [
            {
                'title': 'Добро пожаловать в наш цветочный магазин!',
                'description': 'Создаем красоту для ваших особенных моментов',
                'order': 1
            },
            {
                'title': 'Свежие цветы каждый день',
                'description': 'Работаем только с проверенными поставщиками',
                'order': 2
            },
            {
                'title': 'Быстрая доставка по городу',
                'description': 'Доставляем в течение 2 часов',
                'order': 3
            },
        ]
        
        for slide_data in slider_data:
            slide, created = SliderImage.objects.get_or_create(
                title=slide_data['title'],
                defaults={
                    'description': slide_data['description'],
                    'order': slide_data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Создан слайд: {slide.title}')
        
        # Создаем контактную информацию
        contact, created = Contact.objects.get_or_create(
            address='г. Москва, ул. Цветочная, д. 15, ТЦ "Роза", 1 этаж, павильон 12',
            defaults={
                'phone': '+7 (495) 123-45-67',
                'email': 'info@roza-flowers.ru'
            }
        )
        if created:
            self.stdout.write('Создана контактная информация')
        
        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена тестовыми данными!')
        )
