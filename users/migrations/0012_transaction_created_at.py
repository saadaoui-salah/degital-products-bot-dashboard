# Generated by Django 4.2.7 on 2024-01-24 22:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 1, 24, 22, 13, 13, 123190, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]