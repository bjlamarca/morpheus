# Generated by Django 5.1.3 on 2025-01-18 22:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('utilities', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='systemlog',
            old_name='area',
            new_name='method',
        ),
        migrations.AddField(
            model_name='systemlog',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype', verbose_name='Content Type'),
        ),
        migrations.AddField(
            model_name='systemlog',
            name='module',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
