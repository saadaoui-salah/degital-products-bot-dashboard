# Generated by Django 4.2.7 on 2023-11-30 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_order_code_alter_order_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='created_at',
            new_name='date',
        ),
    ]
