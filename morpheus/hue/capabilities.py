from .hub import Hub
from .models import HueDevice, HueLight

class Capabilities():

    def On(device_id):
        hub = Hub()
        device = HueDevice.objects.get(pk=device_id)
        light = HueLight.objects.get(device=device)
        hub.set_hub(device.hub_id)
        hub.light_set_on('on', light.pk)

    def Off(device_id):
        hub = Hub()
        device = HueDevice.objects.get(pk=device_id)
        light = HueLight.objects.get(device=device)
        hub.set_hub(device.hub_id)
        hub.light_set_on('off', light.pk)

    def Dimmer(device_id, dim_level):
        hub = Hub()
        device = HueDevice.objects.get(pk=device_id)
        light = HueLight.objects.get(device=device)
        hub.set_hub(device.hub_id)
        hub.light_set_dimming(dim_level, light.pk)

    def Color(device_id, red, green, blue):
        hub = Hub()
        device = HueDevice.objects.get(pk=device_id)
        light = HueLight.objects.get(device=device)
        hub.set_hub(device.hub_id)
        hub.light_set_color(red, green, blue, light.pk)
        
