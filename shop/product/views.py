from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .forms import *
from .models import*

menu = ["LKShop", "Каталог", "Корзина", "Войти"]

class ProductHome(ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'jewelries'

    def get_context_data(self, *, object_list=None, **kwargs):
        cats = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['cat_selected']= 0
        context['cats']=cats
        return context

    def get_queryset(self):
        return Product.objects.filter(is_published=True)


# def index(request):
#     jewelries = Product.objects.all()
#     cats = Category.objects.all()
#
#     context = {
#         'jewelries': jewelries,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0
#     }
#     return render(request, 'product/index.html',  context=context)


def about(request):
    return render(request, 'product/about.html',  {'menu': menu, 'title': 'О сайте'})

def addjewelry(request):
    if request.method == 'POST':
        form = AddJewelryForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
            try:
                form.save()
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка!')
    else:
        form = AddJewelryForm()
    return render(request, 'product/addjewelry.html',  {'form': form})

# def show_jewelry(request, jewelry_slug):
#     jewelry = get_object_or_404(Product, slug=jewelry_slug)
#
#     context = {
#         'jewelry': jewelry,
#         'menu': menu,
#         'title': 'Украшение',
#         'cat_selected': jewelry.cat_id,
#     }
#     return render(request, 'product/jewelry.html', context=context)

class ShowJewelry(DetailView):
    model = Product
    template_name = 'product/jewelry.html'
    slug_url_kwarg = 'jewelry_slug'
    context_object_name = 'jewelry'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = context['jewelry']
        context['menu'] = menu
        return context

class ProductCategory(ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'jewelries'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Категория - ' + str(context['jewelries'][0].cat)
        context['menu'] = menu
        context['cat_selected']=context['jewelries'][0].cat_id
        return context

# def show_category(request, cat_id):
#     jewelries = Product.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()
#
#     context = {
#         'jewelries': jewelries,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Страница с категориями',
#         'cat_selected': cat_id
#     }
#     return render(request, 'product/index.html', context=context)
