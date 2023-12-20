from django_filters import FilterSet, DateFilter, CharFilter
from .models import Product
class ProductFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='contains', label='Название')
class Meta:
    model = Product
    fields = ['name', 'cat']

