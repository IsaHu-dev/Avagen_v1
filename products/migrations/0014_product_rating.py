# Generated by Django 3.2.25 on 2025-06-09 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]
