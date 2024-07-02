# Generated by Django 5.0.6 on 2024-06-26 06:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_mascota_remove_customer_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
        migrations.AddField(
            model_name='mascota',
            name='customer',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, related_name='mascotas', to='shop.customer'),
            preserve_default=False,
        ),
    ]
