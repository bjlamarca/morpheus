import django_tables2 as tables
from .models import Scene
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse

class SceneTable(tables.Table):

    class Meta:
        model = Scene
        template_name = "htmx-table.html"
        div_name = 'scene_div'

    def render_name(self, value, record):
         url = reverse('scenes:detail', kwargs={'scene_id':record.pk})
         return format_html("<a hx-get='{}' hx-target='#sc-detail-area' class='link-primary' style='cursor: pointer;'>{}</a>", url, value)
    
class SceneAddTable(tables.Table):
    selected = tables.CheckBoxColumn(accessor='selected')
    dev_name = tables.Column(verbose_name='Name')
    dev_type_display = tables.Column(verbose_name='Device Type')
    dev_id = tables.Column(
           attrs={
            "td": {
                'name': 'dev-id'
            }
        }
    )
    def render_selected(self, record):
        if record['selected']:
            return mark_safe('<input class="nameCheckBox" name="chk-selected" value="' + str(record['dev_id']) + '" type="checkbox" checked/>')
        else:
            return mark_safe('<input class="nameCheckBox" name="chk-selected" value="' + str(record['dev_id']) + '" type="checkbox"/>')
                             
    class Meta:
        template_name = "htmx-table.html"
        div_name = 'scene-add-table-div'

class SceneDeviceTable(tables.Table):
    selected = tables.CheckBoxColumn()
    dev_name = tables.Column(verbose_name='Name')
    dev_type = tables.Column(verbose_name='Device Type')
    switch = tables.Column(verbose_name='Switch')
    dimming = tables.Column(verbose_name='Dimming')
    color_hex = tables.Column(verbose_name='Color')
    
    
    
     
    def render_selected(self, record):

        return mark_safe('<input class="nameCheckBox" name="chk-dev-selected" value="' + str(record['scene_dev_id']) + '" type="checkbox"/>')
    
    def render_color_hex(self, record):
        if 'color' in record['capability']:
            return mark_safe('<span class="badge" style="background-color:' + record['color_hex'] + '; color:' + record['color_hex'] + ';" >The Color</span>')
        else:
            return mark_safe('<span</span>')
    class Meta:
        template_name = "htmx-table.html"
        div_name = 'scene-dev-table-div'
        
    
    
