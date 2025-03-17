import json
from .models import HueDevice, HueLight
from .hub import Hub
from utilities.logging import SystemLogger

logger = SystemLogger('hue', __name__)

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
    try:
        text_data_json = json.loads(text_data)
        device_id = text_data_json['dev_id']    
        device = HueDevice.objects.get(pk=device_id)
        light = HueLight.objects.get(device=device)
        light_dict = {}

        if text_data_json['type'] == 'control':
            hub = Hub()
            print('hub', device.hub_id)
            hub.set_hub(device.hub_id)
            if text_data_json['command'] == 'on':
                hub.light_set_on('on', light.pk)
            if text_data_json['command'] == 'off':
                hub.light_set_on('off', light.pk)
            if text_data_json['command'] == 'dimming':
                hub.light_set_dimming(text_data_json['value'], light.pk)
            if text_data_json['command'] == 'color':
                hex_value = (text_data_json['value']).lstrip('#')
                rgb = tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
                hub.light_set_color(rgb[0], rgb[1], rgb[2], light.pk)
        
        elif text_data_json['type'] == 'update' or text_data_json['type'] == 'open':
            
            light_dict['type'] = 'update'
            if device.hue_device_type == 'COLORLAMP':
                light_dict['is_color'] = 'true'
                light_dict['color_hex'] = "#{:02x}{:02x}{:02x}".format(light.red, light.green, light.blue)
            elif device.hue_device_type == 'WHITELAMP':
                light_dict['is_color'] = 'false'
            light_dict['name'] = device.name
            light_dict['dimming'] = light.dimming
            light_dict['switch'] = (light.switch).capitalize()
            
            
            return light_dict
    except Exception as error:
        logger.log('light_view','Error getting data', error, 'ERROR')
    

def hex_to_rgb(hex):
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal)
  
  return tuple(rgb)


            