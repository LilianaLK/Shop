from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)
    cost = models.IntegerField()
    articul = models.IntegerField()
    weight = models.FloatField(default=10, verbose_name='Вес')
    material = models.CharField(max_length=100, null=True, verbose_name='Материал')
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null = True, related_name='get_jewelries')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jewelry', kwargs={'jewelry_slug': self.slug})
    class Meta:
        verbose_name = 'Украшения'
        verbose_name_plural = 'Украшения'
        ordering =['time_create', 'name']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index= True, verbose_name="Категория")
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering =['id']