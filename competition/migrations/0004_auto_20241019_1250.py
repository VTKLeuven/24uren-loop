# Generated by Django 3.0.8 on 2024-10-19 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_auto_20241017_1939'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rainstatus',
            options={'verbose_name': 'Rain status', 'verbose_name_plural': 'Rain status'},
        ),
        migrations.AddField(
            model_name='runner',
            name='first_year',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
