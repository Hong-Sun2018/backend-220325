# Generated by Django 4.0.3 on 2022-03-26 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_depth',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_length',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_width',
        ),
    ]
