# Generated by Django 5.1.2 on 2024-11-27 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_remove_rented_vehicles_grand_total_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rented_vehicles',
            name='license_image',
        ),
        migrations.AddField(
            model_name='rented_vehicles',
            name='license_file',
            field=models.FileField(blank=True, null=True, upload_to='licenceFile/'),
        ),
    ]
