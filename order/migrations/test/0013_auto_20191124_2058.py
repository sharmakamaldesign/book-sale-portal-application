# Generated by Django 2.2.1 on 2019-11-24 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_auto_20191124_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='product_object',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
    ]