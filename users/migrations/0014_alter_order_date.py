# Generated by Django 4.2.7 on 2024-01-24 22:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_transaction_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 24, 22, 19, 19, 385608, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
