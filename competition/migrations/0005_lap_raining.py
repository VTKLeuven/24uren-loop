# Generated by Django 3.0.8 on 2024-10-19 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0004_auto_20241019_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='lap',
            name='raining',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
