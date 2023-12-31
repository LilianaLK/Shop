from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filter import ProductFilter
from .forms import *
from .models import*
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import ProductSerializer
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
        # добавление других данных
        jewelries = context.get('object_list', [])
        for jewelry in jewelries:
            jewelry.formatted_cost="{:,}".format(jewelry.cost)
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
    paginator = Paginator(contact_list, 3)

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

class ProductAPIList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ProductAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ProductAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)
# class ProductViewSet(viewsets.ModelViewSet):
#     # queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
#
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#         if not pk:
#             return Product.objects.all()
#         return Product.objects.filter(pk=pk)
#
#     # def get_serializer_class(self):
#     #     if self.action == 'retrieve':
#     #         return ProductDetailSerializer
#     #     return ProductSerializer
#
#     @action(methods=['get'], detail=True)
#     def category(self, request,pk=None):
#         cats = Category.objects.get(pk=pk)
#
#         return Response({'cats': cats.name})
#
# class ProductAPIListPagination(PageNumberPagination):
#     page_size = 3
#     page_size_query_param = 'page_size'
#     max_page_size = 10
#
# class ProductAPIList(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = ProductAPIListPagination
# #
# #
# # # class ProductAPIUpdate(generics.UpdateAPIView):
# # #     queryset = Product.objects.all()
# # #     serializer_class = ProductSerializer
# #
# # class ProductAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializer
#
#
# class ProductAPIView(APIView):
#     def get(self, request):
#         p = Product.objects.all()
#         return Response({'jewelries': ProductSerializer(p, many=True).data})
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         jewelry_new = Product.objects.create(
#             name=request.data['name'],
#             description=request.data['description'],
#             cat_id=request.data['cat_id'],
#             cost=request.data['cost'],
#             articul=request.data['articul'],
#             material=request.data['material'],
#             weight=request.data['weight']
#         )
#         return Response({'jewelry': ProductSerializer(jewelry_new).data})
#
#
#
# # class ProductAPIView(generics.ListAPIView):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializer

