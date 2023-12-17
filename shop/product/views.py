from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .filter import ProductFilter
from .forms import *
from .models import*
from .utils import *

class ProductHome(DataMixin, ListView):
    paginate_by = 3
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'jewelries'

    def get_context_data(self, *, object_list=None, auth=None, **kwargs):
        cats = Category.objects.all()
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        st_filter = ProductFilter(self.request.GET, queryset)
        c_def = self.get_user_context(title="Главная страница", st_filter=st_filter)
        auth = self.request.user.is_authenticated
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        # return Product.objects.filter(is_published=True)
        filters = {}
        queryset = super().get_queryset()
        st_filter = ProductFilter(self.request.GET, queryset)
        name = self.request.GET.get('name')
        #
        # if name:
        #     filters['name__contains'] = name
        #
        # new_context = Product.objects.filter(**filters)
        # return new_context
        return st_filter.qs


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
    contact_list = Product.objects.all()
    paginator = Paginator(contact_list, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product/about.html',  {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})



# def addjewelry(request):
#     if request.method == 'POST':
#         form = AddJewelryForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             try:
#                 form.save()
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка!')
#     else:
#         form = AddJewelryForm()
#     return render(request, 'product/addjewelry.html',  {'form': form})

class AddJewelry(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddJewelryForm
    template_name = 'product/addjewelry.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление украшения")
        return dict(list(context.items()) + list(c_def.items()))

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

class ShowJewelry(DataMixin, DetailView):
    model = Product
    template_name = 'product/jewelry.html'
    slug_url_kwarg = 'jewelry_slug'
    context_object_name = 'jewelry'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['jewelry'])
        return dict(list(context.items()) + list(c_def.items()))

class ProductCategory(DataMixin, ListView):
    model = Product
    paginate_by=3
    template_name = 'product/index.html'
    context_object_name = 'jewelries'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(name='Категория - ' + str(context['jewelries'][0].cat),
                                      cat_selected=context['jewelries'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

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



# def login(request):
#     return HttpResponse("Авторизация")
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'product/register.html'
    success_url = reverse_lazy('login')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'product/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

