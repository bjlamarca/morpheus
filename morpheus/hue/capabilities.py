from .hub import Hub
from .models import HueDevice, HueLight
from devices.models import Device
from .color import Converter

class Capabilities():

    def switch(self, device_id, state):
        hub = Hub()
        device = Device.objects.get(pk=device_id)
        hue_device = HueDevice.objects.get(pk=device.device_object_id)
        light = HueLight.objects.get(device=hue_device)
        hub.set_hub(hue_device.hub_id)
        hub.light_set_on(state, light.pk)

    def dimmer(self, device_id, dim_level):
        hub = Hub()
        device = Device.objects.get(pk=device_id)
        hue_device = HueDevice.objects.get(pk=device.device_object_id)
        light = HueLight.objects.get(device=hue_device)
        hub.set_hub(hue_device.hub_id)
        hub.light_set_dimming(dim_level, light.pk)

    def color(self, device_id, red, green, blue):
        hub = Hub()
        device = Device.objects.get(pk=device_id)
        hue_device = HueDevice.objects.get(pk=device.device_object_id)
        light = HueLight.objects.get(device=hue_device)
        hub.set_hub(hue_device.hub_id)
        hub.light_set_color(red, green, blue, light.pk)

    def activate_scene(self, scene_dev_list):
        for scene_dev in scene_dev_list:
            print(scene_dev)
            
    def get_on(self, device_id):
        hub = Hub()
        device = Device.objects.get(pk=device_id)
        hue_device = HueDevice.objects.get(pk=device.device_object_id)
        light = HueLight.objects.get(device=hue_device)
        hub.set_hub(hue_device.hub_id)
        light_item = hub.get_item('light',light.rid)
        return bool(light_item['on']['on'])
    
    def get_dim(self, device_id):
        hub = Hub()
        device = Device.objects.get(pk=device_id)
        hue_device = HueDevice.objects.get(pk=device.device_object_id)
        light = HueLight.objects.get(device=hue_device)
        hub.set_hub(hue_device.hub_id)
        light_item = hub.get_item('light',light.rid)
        return int(light_item['dimming']['brightness'])
    
    def get_color(self, device_id):
        hub = Hub()
        device = Device.objects.get(pk=device_id)
        hue_device = HueDevice.objects.get(pk=device.device_object_id)
        light = HueLight.objects.get(device=hue_device)
        hub.set_hub(hue_device.hub_id)
        light_item = hub.get_item('light',light.rid)
        convert = Converter(light.gamut_type)
        rgb = convert.xy_to_rgb(light_item['color']['xy']['x'], light_item['color']['xy']['y'])
        return [rgb[0], rgb[1], rgb[2]]

        
