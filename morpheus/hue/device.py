import json
from .models import HueDevice, HueLight
from .hub import Hub

class Capability():
    def On(self, state):
        print(state)


class HueDeviceTypes():
    #
    def __init__(self):
        self.device_list = [
            {
                'display_name': 'White Light',
                'hue_device_type': 'WHITELAMP',
                'morph_name': 'HUEWHITELAMP',
                'morph_display_name': 'Hue White Light',
                'capability': 'switch, dimmer',
                'morph_sync': True

            },
            {
                'display_name': 'Color Light',
                'hue_device_type': 'COLORLAMP',
                'morph_name': 'HUECOLORLAMP',
                'morph_display_name': 'Hue Color Light',
                'capability': 'color, switch, dimmer',
                'morph_sync': True

            },
            {
                'display_name': 'Dimmer Switch',
                'hue_device_type': 'DIMSWITCH',
                'morph_name': 'HUEDIMSWITCH',
                'morph_display_name': 'Hue Dimmer Switch',
                'morph_sync': False

            },
            {
                'display_name': 'Hub',
                'hue_device_type': 'HUB',
                'morph_name': 'HUEHUB',
                'morph_display_name': 'Hue Hub',
                'morph_sync': False

            },
            
        ]
    def get_device_list(self):
        return self.device_list
    

def light_view(text_data):
    
    text_data_json = json.loads(text_data)
    device_id = text_data_json['dev_id']    
    device = HueDevice.objects.get(pk=device_id)
    light = HueLight.objects.get(device=device)
    
    if text_data_json['type'] == 'control':
        hub = Hub()
        print('hub', device.hub_id)
        hub.set_hub(device.hub_id)
        print(text_data_json['dev_id'])
        if text_data_json['command'] == 'on':
            hub.light_set_on('on', light.pk)
        if text_data_json['command'] == 'off':
            hub.light_set_on('off', light.pk)
    
    elif text_data_json['type'] == 'update':
        light_dict = {}
        
        if device.hue_device_type == 'COLORLAMP':
            light_dict['is_color'] = 'true'
        elif device.hue_device_type == 'WHITELAMP':
            light_dict['is_color'] == 'false'
        light_dict['name'] = device.name
        light_dict['dimming'] = light.dimming
        if light.light_on == True:
            light_dict['light_on'] = 'On'
        elif light.light_on == False:
            light_dict['light_on'] = 'Off'
        
        
        return light_dict
            