import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
django.setup()

from main.models import Product, SliderImage

# Обновляем товары с изображениями
products = Product.objects.all()
product_images = [
    'roses.jpg',
    'roses.jpg',  # белые розы
    'tulips.jpg',
    'lilies.jpg',
    'mixed.jpg',  # хризантемы
    'mixed.jpg',  # герберы
]

for i, product in enumerate(products):
    if i < len(product_images):
        product.image = f'products/{product_images[i]}'
        product.save()
        print(f'Обновлен товар: {product.name}')

# Обновляем слайды с изображениями
slider_images = SliderImage.objects.all()
slider_files = ['slider1.jpg', 'slider2.jpg', 'slider3.jpg']

for i, slide in enumerate(slider_images):
    if i < len(slider_files):
        slide.image = f'slider/{slider_files[i]}'
        slide.save()
        print(f'Обновлен слайд: {slide.title}')

print('Все изображения обновлены!')
