# Generated by Django 2.2.1 on 2019-09-28 10:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]