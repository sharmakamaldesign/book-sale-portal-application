# Generated by Django 2.2.1 on 2019-09-28 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_delivered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
