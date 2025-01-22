# Generated by Django 5.1.3 on 2025-01-21 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenetile',
            name='page_section',
        ),
        migrations.RemoveField(
            model_name='scenetile',
            name='scene',
        ),
        migrations.RemoveField(
            model_name='scenetile',
            name='tile_type',
        ),
        migrations.RemoveField(
            model_name='pagesection',
            name='tile_size',
        ),
        migrations.RemoveField(
            model_name='tiletype',
            name='tile_size',
        ),
        migrations.RemoveField(
            model_name='tile',
            name='tile_type',
        ),
        migrations.RemoveField(
            model_name='tile',
            name='sort',
        ),
        migrations.RemoveField(
            model_name='tile',
            name='tyle_type_id',
        ),
        migrations.DeleteModel(
            name='NavTile',
        ),
        migrations.DeleteModel(
            name='SceneTile',
        ),
        migrations.DeleteModel(
            name='TileSize',
        ),
        migrations.DeleteModel(
            name='TileType',
        ),
    ]
