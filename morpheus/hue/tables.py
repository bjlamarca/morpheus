import django_tables2 as tables
from .models import Device, Light

class DeviceTable(tables.Table):
    class Meta:
        model = Device
        fields = ('name', 'hue_device_type', 'online', 'last_checkin')
        template_name = "htmx-table.html"

class LightTable(tables.Table):
    online = tables.BooleanColumn(
        accessor='device.online'
        )
    #dimming = tables.Column(attrs={'cell': {'style': 'background-color: blue'}})
    class Meta:
        model = Light
        fields = ('device', 'light_on', 'dimming', 'red', 'green', 'blue', 'online')
        template_name = "htmx-table.html"
        
        