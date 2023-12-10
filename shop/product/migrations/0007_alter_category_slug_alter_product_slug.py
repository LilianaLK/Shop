# Generated by Django 4.2.7 on 2023-12-10 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_category_slug_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
    ]