import django_tables2 as tables
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db import models
from .models import Device, DeviceType

class DeviceTable(tables.Table):
    #name = tables.Column(linkify=True)
    #name = tables.LinkColumn()
    interface_name = tables.Column(
        verbose_name='Interface')
    class Meta:
        model = Device
        div_name = 'device_div'
        fields = ('name', 'interface_name', 'device_type')
        template_name = "htmx-table.html"

    def render_name(self, value, record):
         url = reverse('devices:device-detail', kwargs={'device_id':record.pk})
         return format_html("<a hx-get='{}' hx-target='#dev-detail-area' class='link-primary' style='cursor: pointer;'>{}</a>", url, value)
    
class DeviceColorTable(tables.Table):
    favorite = tables.CheckBoxColumn()
    name = tables.Column(
        verbose_name='Name')
    hex_code = tables.Column(
        verbose_name='Color')
    color_family = tables.ManyToManyColumn(
        verbose_name='Family'
    )

    def render_favorite(self, record):
        if record.favorite:
            return mark_safe('<input class="nameCheckBox" name="chk-favorite" value="' + str(record.pk) + '" type="checkbox" checked/>')
        else:
            return mark_safe('<input class="nameCheckBox" name="chk-favorite" value="' + str(record.pk) + '" type="checkbox"/>')
        pass
        
    
    def render_hex_code(self, record):
        return mark_safe('<span class="badge" style="background-color:' + record.hex_code + '; color:' + record.hex_code + ';" >The Color</span>')
    class Meta:
        div_name = 'device_color_div'
        template_name = "htmx-table.html"