# Generated by Django 4.2.7 on 2024-02-10 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_code_created_at_alter_package_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='choices',
            field=models.CharField(choices=[('NORMAL', 'Normal'), ('IN DEMAND', 'In Demand')], default='NORMAL', max_length=100),
        ),
    ]