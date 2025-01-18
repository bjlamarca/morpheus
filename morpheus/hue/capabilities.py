from .hub import Hub
from .models import HueDevice, HueLight
from devices.models import Device
from .color import Converter
import time

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
            hub = Hub()
            device = Device.objects.get(pk=scene_dev['device_id'])
            hue_device = HueDevice.objects.get(pk=device.device_object_id)
            light = HueLight.objects.get(device=hue_device)
            hub.set_hub(hue_device.hub_id)
            if hue_device.hue_device_type == 'COLORLAMP':
                hub.light_set_color_dim_on(scene_dev['color'][0], scene_dev['color'][1], scene_dev['color'][2], scene_dev['dimmer'], scene_dev['switch'], light.pk)
            elif hue_device.hue_device_type == 'WHITELAMP':
                hub.light_set_dim_on(scene_dev['dimmer'], scene_dev['switch'], light.pk)
            time.sleep(0.1)
            
    def get_on(self, device_id):
        hub = Hub()
        device = Device.objects.get(pk=device_id)
        hue_device = HueDevice.objects.get(pk=device.device_object_id)
        light = HueLight.objects.get(device=hue_device)
        hub.set_hub(hue_device.hub_id)
        light_item = hub.get_item('light',light.rid)
        if light_item['on']['on'] == True:
            return 'on'
        elif light_item['on']['on'] == False:
            return 'off'
    
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

        
