import json
from .models import Device, Light, Button
from .hub import Hub
from .color import Converter
from decimal import Decimal
from utilities.logging import SystemLogger
from django.shortcuts import get_object_or_404

class DeviceType():
    HUE_DEVICE_TYPE = [
        ['WHITELAMP', 'White Lamp'],
        ['COLORLAMP', 'Color Lamp'],
        ['DIMSWITCH', 'Dimmer Switch'],
        ['HUB', 'Hue Hub']
    ]
    #Hue zigbee Model ID, Morpheus Hue Device Type, Morpheus Device Type 
    DEVICE_TYPE = [
        ['LCA009','COLORLAMP','LIGHT-COLOR'],
        ['LCT014','COLORLAMP','LIGHT-COLOR'],
        ['LCA003','COLORLAMP','LIGHT-COLOR'],
        ['LWB014','WHITELAMP','LIGHT-WHITE'],
        ['LCA002','COLORLAMP','LIGHT-COLOR'],
        ['BSB002','HUB','HUE-HUB'],
        ['LCA005','COLORLAMP','LIGHT-COLOR'],
        ['LCT016','COLORLAMP','LIGHT-COLOR'],
        ['RWL020','DIMSWITCH','SWITCH-COLOR'],
    ]

    def huetype_from_modelid(self, model_id):
        exists = False
        for model in self.DEVICE_TYPE:
            if model_id == model[0]:
                exists = True
                break
        if exists:
            return model[1]
        else:
            return None
        

class HueDevice():

    def __init__(self):
        self.hub_id = ''
        self.device_dict = {}
    
    def sync_device_db(self, hub_id):
        self.hub_id = hub_id
        hub = Hub()
        hub.set_hub(self.hub_id)
        devices = hub.get_items('devices')
        for device in devices:
            device_qs = Device.objects.filter(hue_id=device['id'])
            if device_qs:
                device_qs[0].name = device['metadata']['name']
                device_qs[0].software_version = device['metadata']['name']
                device_qs[0].save()
            else:
                #create parent device
                new_device = Device(
                    product_name = device['product_data']['product_name'],
                    hub_id = hub_id,
                    hue_id = device['id'],
                    model_id = device['product_data']['model_id'],
                    manufacturer_name = device['product_data']['manufacturer_name'],
                    software_version = device['product_data']['software_version'],
                    name = device['metadata']['name'],
                )
                services = device['services']
                #Get the zigbee service rid
                for service in services:
                    service_dict = dict(service)
                    if service_dict['rtype'] == 'zigbee_connectivity':
                        new_device.zigbee_rid = service_dict['rid']

                #get the device type, add it
                device_type = DeviceType()
                hue_type = device_type.huetype_from_modelid(device['product_data']['model_id'])
                new_device.hue_device_type = hue_type
                
                if hue_type == 'COLORLAMP' or hue_type == 'WHITELAMP':
                    new_light = Light()
                    new_device.save()
                    new_light.device = new_device
                    for service in services:
                        service_dict = dict(service)
                        if service_dict['rtype'] == 'light':
                            new_light.rid = service_dict['rid']
                            if hue_type == 'COLORLAMP':
                                #get light details from Hub to get Gamut
                                light_item = hub.get_item('light',service_dict['rid'])
                                new_light.gamut_type = light_item['color']['gamut_type']
                    new_light.save()
                
                if hue_type == 'DIMSWITCH':
                    #A switch will have multiple buttons and a power state rid
                    new_device.save()
                    button_num = 1
                    for service in services:
                        service_dict = dict(service)
                        if service_dict['rtype'] == 'device_power':
                            new_device.power_rid = service_dict['rid']
                            new_device.save()
                        if service_dict['rtype'] == 'button':
                            new_button = Button()
                            new_button.device = new_device
                            new_button.rid = service_dict['rid']
                            new_button.name = 'Button ' + str(button_num)
                            button_num += 1
                            new_button.save()

                if hue_type == 'HUB':
                    new_device.save()
                    for service in services:
                        service_dict = dict(service)
                        if service_dict['rtype'] == 'bridge':
                            new_device.bridge_rid = service_dict['rid']
                            new_device.save()

                     
                else:
                    #device type not found
                    sys_log = SystemLogger('Sync Databse','Item type not found, not added to DB', 
                                           'Hue Type: ' + device['product_data']['model_id'], 'ERROR')
                    sys_log.log()   

    def update_device_status(self, device_id, hub_id):
        try:
            device = Device.objects.get(pk=device_id)
            hub = Hub()
            hub.set_hub(hub_id)

            print(device.hue_device_type)
            if device.hue_device_type == 'COLORLAMP' or device.hue_device_type == 'WHITELAMP':
                light_qs = Light.objects.get(device=device)
                print('qs', light_qs.rid)
                light_item = hub.get_item('light',light_qs.rid)
                #print('TYPE', light_item)
                print('LI' )
                light_qs.light_on = bool(light_item['on']['on'])
                light_qs.dimming =  Decimal(light_item['dimming']['brightness'])
                light_qs.effect = light_item['effects']['status']
                if device.hue_device_type == 'COLORLAMP':
                    convert = Converter(light_qs.gamut_type)
                    rgb = convert.xy_to_rgb(light_item['color']['xy']['x'], light_item['color']['xy']['y'])
                    light_qs.red = rgb[0]
                    light_qs.green = rgb[1]
                    light_qs.blue = rgb[2]
                light_qs.save()
        except Exception as error:
            sys_log = SystemLogger('HueDevice','update_device_status', str(error), 'ERROR')
            sys_log.log()       

    def update_all_device_status(self, hub_id):
        try: 
            devices = Device.objects.all()
            for device in devices:
                self.update_device_status(device.pk, hub_id)

        except Exception as error:
            sys_log = SystemLogger('HueDevice','update_device_status', str(error), 'ERROR')
            sys_log.log()    


        
        
        
        

        

                
                    
                    
                

            
            
            
                
        
        
        
        