import django_tables2 as tables
from .models import Page, PageSection, Tile
from django.urls import reverse
from django.utils.html import format_html

class PageTable(tables.Table):
    class Meta:
        model = Page
        template_name = 'htmx-table.html'
        dive_name = 't-page_div'

    def render_name(self, value, record):
        url = reverse('tiles:detail', kwargs={'page_id':record.pk})
        return format_html("<a hx-get='{}' hx-target='#t-page-area' class='link-primary' style='cursor: pointer;'>{}</a>", url, value)
    
class PageSectionTable(tables.Table):
    class Meta:
        model = PageSection
        template_name = 'htmx-table.html'
        dive_name = 't-section_div'

    def render_name(self, value, record):
        url = reverse('tiles:section-detail', kwargs={'section_id':record.pk})
        return format_html("<a hx-get='{}' hx-target='#t-page-area' class='link-primary' style='cursor: pointer;'>{}</a>", url, value)
    
class TileTable(tables.Table):
    class Meta:
        model = Tile
        template_name = 'htmx-table.html'
        dive_name = 't-tile_div'

    def render_name(self, value, record):
        url = reverse('tiles:tile-detail', kwargs={'tile_id':record.pk})
        return format_html("<a hx-get='{}' hx-target='#t-page-area' class='link-primary' style='cursor: pointer;'>{}</a>", url, value)
    
    # def render_tile_type(self, value, record):
    #     return record.get_tile_type_display()
    
    # def render_tile_object_id(self, value, record):
    #     return record.tile_object_id
    
    