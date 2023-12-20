from product.models import *

menu = [{'name': "LKShop", 'url_name': 'about'},
        {'name': "Корзина", 'url_name': 'home'},
]

class DataMixin:
    paginate_by=3
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context['menu'] = menu
        context['cats']=cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

