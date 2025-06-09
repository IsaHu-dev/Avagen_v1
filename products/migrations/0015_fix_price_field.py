from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='base_price',
            field=models.DecimalField(max_digits=6, decimal_places=2, null=False),
        ),
    ] 