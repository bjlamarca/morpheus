# Generated by Django 5.1.3 on 2025-01-01 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hue', '0006_device_battery_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='event',
            field=models.CharField(blank=True, default=None, null=True, verbose_name='Last Event'),
        ),
        migrations.AddField(
            model_name='button',
            name='updated',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Last Update'),
        ),
        migrations.AlterField(
            model_name='device',
            name='battery_level',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Battery Level'),
        ),
    ]
