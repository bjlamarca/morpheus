# Generated by Django 5.1.3 on 2025-01-13 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenedevices',
            name='scene_device_type',
            field=models.CharField(blank=True, choices=[('COLOR', 'Color'), ('DIMMER', 'Dimmer'), ('SWITCH', 'Switch')], max_length=20, null=True, verbose_name='Device Type'),
        ),
    ]
