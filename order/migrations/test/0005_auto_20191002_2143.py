# Generated by Django 2.2.1 on 2019-10-02 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_deliverycharge'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='calceledDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='canceled',
            field=models.BooleanField(default=False),
        ),
    ]