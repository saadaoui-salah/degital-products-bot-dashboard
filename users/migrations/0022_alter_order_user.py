# Generated by Django 4.2.1 on 2024-02-25 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_order_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(limit_choices_to={'is_admin': False}, on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to='users.user'),
        ),
    ]