# Generated by Django 5.0.1 on 2024-01-26 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_transaction_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='added_to_group',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_member',
            field=models.BooleanField(default=False),
        ),
    ]
