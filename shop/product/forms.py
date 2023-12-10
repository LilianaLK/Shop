from django import forms
from django.core.exceptions import ValidationError

from .models import *
class AddJewelryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label ='Не выбрана'

    class Meta:
        model = Product
        fields = ['name', 'cost', 'articul','photo', 'weight', 'material', 'is_published', 'description', 'slug', 'cat']

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.isalpha():
            raise ValidationError('Недопустимые символы')
        return name
