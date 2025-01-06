import django_tables2 as tables
from .models import HueDevice, HueLight, HueButton

class DeviceTable(tables.Table):
    class Meta:
        model = HueDevice
        div_name = 'device_div'
        fields = ('name', 'hue_device_type', 'online', 'battery_level')
        template_name = "htmx-table.html"

class LightTable(tables.Table):
    online = tables.BooleanColumn(
        accessor='device.online'
        )
    
    #dimming = tables.Column(attrs={'cell': {'style': 'background-color: blue'}})
    class Meta:
        model = HueLight
        div_name = 'light_div'
        fields = ('id','device', 'light_on', 'dimming', 'red', 'green', 'blue', 'online')
        template_name = "htmx-table.html"
        
class ButtonTable(tables.Table):
    online = tables.BooleanColumn(
        accessor='device.online'
        )
    class Meta:
        model = HueButton
        div_name = 'button_div'
        fields = ('device', 'name', 'event', 'updated', 'online')
        template_name = "htmx-table.html"
        