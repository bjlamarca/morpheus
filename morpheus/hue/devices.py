import json
from .models import Device, Light, Button
from .hub import Hub
from .color import Converter

class ProductTypes():
    DEVICE_TYPE = (
        ('WHITELAMP', 'White Lamp'),
        ('COLORLAMP', 'Color Lamp'),
        ('DIMSWITCH', 'Dimmer Switch'),
        ('HUB', 'Hue Hub')

    )

    MODEL_ID = (
        ('LCA009'),
        ('LCT014'),
        ('LCA003'),
        ('LWB014'),
        ('LCA002'),
        ('BSB002'),
        ('LCA005'),
        ('LCT016'),
        ('RWL020'),
    )

    PRODUCT_NAME = (
        'Hue dimmer switch',
        'Hue color lamp',
        'Hue white lamp',
    )

    def __iter__(self):
        return iter(self.PRODUCT_NAME)

class HueDevice():

    def __init__(self):
        
        self.product_name = ''
        self.hub_id = ''
        self.hue_id = ''
        self.model_id = ''
        self.manufacturer_name = ''
        self.software_version = ''
        self.name = ''
        self.gamut_type = ''
        self.device_dict = {}
    
    def add_device(self):
        #create parent device
        new_device = Device(
                product_name = self.device_dict['product_data']['product_name'],
                hub_id = self.hub_id,
                hue_id = self.device_dict['id'],
                model_id = self.device_dict['product_data']['model_id'],
                manufacturer_name = self.device_dict['product_data']['manufacturer_name'],
                software_version = self.device_dict['product_data']['software_version'],
                name = self.device_dict['metadata']['name'],
        
        )
        new_device.save()
        print('--', new_device)
        #create Light or Button records, update fields in parent based on services
        button_num = 1
        services = self.device_dict['services']
        #if self.product_name == 'Hue color lamp' or self.product_name == 'Hue white lamp':
        for service in services:
            service_dict = dict(service)
            if service_dict['rtype'] == 'zigbee_connectivity':
                new_device.zigbee_rid = service_dict['rid']
            if service_dict['rtype'] == 'light':
                #get the light for Gamut (if color), and current status
                hub = Hub()
                hub.set_hub(self.hub_id)
                light_rid = service_dict['rid']
                light = hub.get_light(light_rid)
                #print('Light', json.dumps(light, indent=2))
                
                new_light = Light()
                new_light.rid = light_rid
                new_light.device = new_device
                new_light.light_on = light['on']['on']
                new_light.dimming = light['dimming']['brightness']
                #check if color device
                if 'color' in light:
                    new_light.color_enabled = True
                    gamut = light['color']['gamut_type']
                    #get x,y and convert it to RGB
                    convert = Converter(gamut)
                    print('Detail:', light['color']['xy']['x'], light['color']['xy']['y']) 
                    rgb = convert.xy_to_rgb(light['color']['xy']['x'], light['color']['xy']['y'])
                    new_light.red = rgb[0]
                    new_light.green = rgb[1]
                    new_light.blue = rgb[2]
                    new_light.gamut_type = gamut
                else:
                    new_light.color_enabled = False
                new_light.save()
            if service_dict['rtype'] == 'device_power':
                new_device.power_rid = service_dict['rid']
            if service_dict['rtype'] == 'button':
                new_button = Button()
                new_button.device = new_device
                new_button.rid = service_dict['rid']
                new_button.name = 'Button ' + str(button_num)
                button_num += 1
                new_button.save()
        new_device.save()

                
                    
                    
                

            
            
            
                
        
        
        
        