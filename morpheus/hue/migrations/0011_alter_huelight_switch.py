# Generated by Django 5.1.3 on 2025-01-16 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hue', '0010_huelight_switch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='huelight',
            name='switch',
            field=models.CharField(blank=True, choices=[('on', 'On'), ('off', 'Off')], max_length=50, null=True, verbose_name='Switch'),
        ),
    ]
