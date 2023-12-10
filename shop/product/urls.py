from django.urls import path, re_path

from .views import *
urlpatterns = [
    path('', ProductHome.as_view(), name='home'),
    path('about/', about, name='about'),
    # path('jewelry/<int:jewelry_id>/', show_jewelry, name='jewelry'),
    path('category/<slug:cat_slug>/', ProductCategory.as_view(), name='category'),
    path('jewelry/<slug:jewelry_slug>/', ShowJewelry.as_view(), name='jewelry'),
    path('addjewelry/', AddJewelry.as_view(), name='addjewelry')
]

