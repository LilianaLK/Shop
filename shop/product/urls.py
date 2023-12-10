from django.urls import path, re_path

from .views import *
urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('jewelry/<int:jewelry_id>/', show_jewelry, name='jewelry'),
    path('category/<int:cat_id>/', show_category, name='category')
]

