# Generated by Django 5.1.3 on 2025-01-15 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hue', '0009_rename_button_huebutton_rename_device_huedevice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='huelight',
            name='switch',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Switch'),
        ),
    ]
