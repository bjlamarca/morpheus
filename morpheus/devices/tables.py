import django_tables2 as tables
from django.utils.html import format_html
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