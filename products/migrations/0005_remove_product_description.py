# Generated by Django 4.2.7 on 2023-11-17 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
    ]
