# Generated by Django 5.1.2 on 2024-11-09 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='bike',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.bike'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.car'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='delivery_type',
            field=models.CharField(blank=True, choices=[('pickup', 'Self Pickup'), ('delivery', 'Delivery')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='license_image',
            field=models.ImageField(blank=True, null=True, upload_to='licenceImage/'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='pick_delivery_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='pickup_delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='return_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]