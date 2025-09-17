from PIL import Image, ImageDraw, ImageFont
import os

# Создаем папки если их нет
os.makedirs('static/images', exist_ok=True)
os.makedirs('media/products', exist_ok=True)
os.makedirs('media/slider', exist_ok=True)

# Создаем изображения для товаров
products = [
    ('roses.jpg', 'Розы', (255, 0, 0)),
    ('tulips.jpg', 'Тюльпаны', (255, 165, 0)),
    ('lilies.jpg', 'Лилии', (255, 255, 255)),
    ('mixed.jpg', 'Смешанный букет', (128, 0, 128)),
]

for filename, name, color in products:
    # Создаем изображение 400x300
    img = Image.new('RGB', (400, 300), color)
    draw = ImageDraw.Draw(img)
    
    # Добавляем текст
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Получаем размеры текста
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Центрируем текст
    x = (400 - text_width) // 2
    y = (300 - text_height) // 2
    
    # Рисуем текст
    draw.text((x, y), name, fill=(255, 255, 255), font=font)
    
    # Сохраняем в static/images
    img.save(f'static/images/{filename}')
    # Копируем в media/products
    img.save(f'media/products/{filename}')

# Создаем изображения для слайдера
slider_images = [
    ('slider1.jpg', 'Добро пожаловать!', (220, 53, 69)),
    ('slider2.jpg', 'Свежие цветы', (40, 167, 69)),
    ('slider3.jpg', 'Быстрая доставка', (0, 123, 255)),
]

for filename, name, color in slider_images:
    # Создаем изображение 800x400
    img = Image.new('RGB', (800, 400), color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    # Получаем размеры текста
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Центрируем текст
    x = (800 - text_width) // 2
    y = (400 - text_height) // 2
    
    # Рисуем текст
    draw.text((x, y), name, fill=(255, 255, 255), font=font)
    
    # Сохраняем в media/slider
    img.save(f'media/slider/{filename}')

print("Изображения созданы успешно!")
