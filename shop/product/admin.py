from django.contrib import admin

# Register your models here.

from .models import *

class ProductAdmin(admin.ModelAdmin):
 list_display = ('id', 'name', 'time_create', 'is_published', 'photo')
 list_display_links = ('id', 'name')
 search_fields = ('name', 'name')
 prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
 list_display = ('id', 'name')
 list_display_links = ('id', 'name')
 search_fields = ('name', )
 prepopulated_fields = {"slug": ("name",)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)


