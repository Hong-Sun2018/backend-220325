# Generated by Django 4.0.3 on 2022-03-26 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_product_depth_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='id',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
