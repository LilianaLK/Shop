from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import*

menu = ["LKShop", "Каталог", "Корзина", "Войти"]
def index(request):
    jewelries = Product.objects.all()
    cats = Category.objects.all()

    context = {
        'jewelries': jewelries,
        'cats': cats,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0
    }
    return render(request, 'product/index.html',  context=context)


def about(request):
    return render(request, 'product/about.html',  {'menu': menu, 'title': 'О сайте'})

def show_jewelry(request, jewelry_id):
    jewelry = Product.objects.filter(id=jewelry_id)
    jewerly = get_object_or_404(Product, pk=jewelry_id)

    context = {
        'jewelry': jewelry,
        'menu': menu,
        'title': 'Украшение',
        'cat_selected': jewerly.cat_id,
    }
    return render(request, 'product/jewelry.html', context=context)

def show_category(request, cat_id):
    jewelries = Product.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    context = {
        'jewelries': jewelries,
        'cats': cats,
        'menu': menu,
        'title': 'Страница с категориями',
        'cat_selected': cat_id
    }
    return render(request, 'product/index.html', context=context)
