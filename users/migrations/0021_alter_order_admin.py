# Generated by Django 4.2.1 on 2024-02-25 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_order_admin_report_order_alter_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='admin',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_admin': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_user', to='users.user'),
        ),
    ]