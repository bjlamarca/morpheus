from django.db import models
from scenes.models import Scene
from .choices import PageTypes, TileTypes

page_types = PageTypes()
tile_types = TileTypes()

class Page(models.Model):
    name = models.CharField(max_length=100)
    page_type = models.CharField(
        max_length=100,
        choices=page_types.get_page_types_choices(),
    )

    def __str__(self):
        return self.name

class PageSection(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
        )
    page = models.ForeignKey(
        Page, 
        on_delete=models.CASCADE
    )
    sort = models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Tile(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
        )
    page_section = models.ForeignKey(
        PageSection, 
        on_delete=models.CASCADE
    )
    tile_type = models.CharField(
        max_length=100,
        choices=tile_types.get_tile_types_choices(),
       )
    tile_object_id = models.IntegerField()   
    
    sort = models.IntegerField()