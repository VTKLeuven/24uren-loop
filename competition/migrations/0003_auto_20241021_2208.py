# Generated by Django 3.0.8 on 2024-10-21 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0002_auto_20211107_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lap',
            name='runner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='laps', to='competition.Runner'),
        ),
    ]