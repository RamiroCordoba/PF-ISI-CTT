# Generated by Django 5.0.4 on 2025-05-31 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_alter_producto_stock_optimo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='stock_optimo',
        ),
    ]
