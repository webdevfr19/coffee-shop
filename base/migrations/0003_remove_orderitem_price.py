# Generated by Django 4.2 on 2023-06-29 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_cart_products_cart_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
    ]
