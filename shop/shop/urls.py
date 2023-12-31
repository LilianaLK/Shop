"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from product.views import *
from django.urls import path, include
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/product/',ProductAPIList.as_view()),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/product/<int:pk>/',ProductAPIUpdate.as_view()),
    path('api/v1/productdelete/<int:pk>/',ProductAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),


    # path('', include('product.urls')),
    # path('api/v1/', include(router.urls)),
    # path('api/v1/productDetail/', ProductAPIList.as_view()),
    #
    # path('api/v1/productlist/', ProductViewSet.as_view({'get': 'list'})),
    # path('api/v1/productlist/<int:pk>/', ProductViewSet.as_view({'put': 'update'})),
    # path('api/v1/productdetail/<int:pk>/', ProductAPIDetailView.as_view()),

    path('product/', include('product.urls')),

]


if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL,
 document_root=settings.MEDIA_ROOT)
