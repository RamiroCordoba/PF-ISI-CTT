# Generated by Django 5.0.4 on 2025-05-31 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_remove_producto_stock_optimo'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='stock_optimo',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
