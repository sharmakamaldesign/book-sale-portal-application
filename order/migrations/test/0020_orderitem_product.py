# Generated by Django 2.2.1 on 2019-12-10 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20191209_1914'),
        ('order', '0019_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
            preserve_default=False,
        ),
    ]
