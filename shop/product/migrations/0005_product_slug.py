# Generated by Django 4.2.7 on 2023-12-10 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL'),
        ),
    ]
