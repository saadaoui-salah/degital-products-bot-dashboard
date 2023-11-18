# Generated by Django 3.2.13 on 2023-11-16 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20231116_1446'),
        ('users', '0002_alter_user_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='amount',
            new_name='balance',
        ),
        migrations.AddField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='tg_id',
            field=models.CharField(default=123, max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='tg_username',
            field=models.CharField(default=132, max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.package')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]
