# Generated by Django 5.0.6 on 2024-06-13 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]