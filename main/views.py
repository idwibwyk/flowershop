from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, SliderImage, Contact


def home(request):
    """Главная страница"""
    slider_images = SliderImage.objects.filter(is_active=True).order_by('order')
    context = {
        'slider_images': slider_images,
    }
    return render(request, 'main/home.html', context)


def catalog(request):
    """Страница каталога"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Сортировка
    sort_by = request.GET.get('sort')
    if sort_by == 'year':
        products = products.order_by('-year')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'price':
        products = products.order_by('price')
    else:
        products = products.order_by('-created_at')  # По умолчанию по новизне
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_id,
        'current_sort': sort_by,
    }
    return render(request, 'main/catalog.html', context)


def product_detail(request, product_id):
    """Страница товара"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    context = {
        'product': product,
    }
    return render(request, 'main/product_detail.html', context)


def contacts(request):
    """Страница контактов"""
    contact_info = Contact.objects.first()
    context = {
        'contact_info': contact_info,
    }
    return render(request, 'main/contacts.html', context)