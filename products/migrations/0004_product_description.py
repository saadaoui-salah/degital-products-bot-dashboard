# Generated by Django 4.2.7 on 2023-11-17 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20231116_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='sdsdsdsd'),
            preserve_default=False,
        ),
    ]
