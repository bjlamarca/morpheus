# Generated by Django 5.1.3 on 2025-01-21 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiles', '0002_remove_scenetile_page_section_remove_scenetile_scene_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='page_type',
        ),
        migrations.AddField(
            model_name='tile',
            name='sort',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PageType',
        ),
    ]
