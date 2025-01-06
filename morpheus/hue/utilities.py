import json
from .models import HueDevice, HueLight, HueButton
from .hub import Hub
from .color import Converter
from decimal import Decimal
from utilities.logging import SystemLogger
from django.shortcuts import get_object_or_404
from .device import HueDeviceTypes
from devices.models import Device, DeviceType

        
      

class HueUtilities():

    def __init__(self):
        self.hub_id = ''
        self.device_dict = {}

    def huetype_from_modelid(self, model_id):
        
        HUE_MODEL_TYPE = [
            ['LCA009','COLORLAMP'],
            ['LCT014','COLORLAMP'],
            ['LCA003','COLORLAMP'],
            ['LWB014','WHITELAMP'],
            ['LCA002','COLORLAMP'],
            ['BSB002','HUB'],
            ['LCA005','COLORLAMP'],
            ['LCT016','COLORLAMP'],
            ['RWL020','DIMSWITCH'],
        ]

        exists = False
        for model in HUE_MODEL_TYPE:
            if model_id == model[0]:
                exists = True
                break
        if exists:
            return model[1]
        else:
            return None
    
    def sync_device_db(self, hub_id):
        try:
            self.hub_id = hub_id
            hub = Hub()
            hub.set_hub(self.hub_id)
            devices = hub.get_items('devices')
            for device in devices:
                device_qs = HueDevice.objects.filter(hue_id=device['id'])
                if device_qs:
                    device_qs[0].name = device['metadata']['name']
                    device_qs[0].software_version = device['product_data']['software_version']
                    device_qs[0].save()
                else:
                    #create parent device
                    new_device = HueDevice(
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
                    
                    hue_type = self.huetype_from_modelid(device['product_data']['model_id'])
                    new_device.hue_device_type = hue_type
                    
                    if hue_type == 'COLORLAMP' or hue_type == 'WHITELAMP':
                        new_light = HueLight()
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
                                new_button = HueButton()
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
                        sys_log = SystemLogger(__name__,'Sync Databse: Item type not found, not added to DB', 
                                            'Hue Type: ' + device['product_data']['model_id'], 'ERROR')
                        sys_log.log()
            return 'Database Sync Complete'
        except Exception as error:
            sys_log = SystemLogger(__name__,'update_device_status', str(error), 'ERROR')
            sys_log.log()
            return str(error)   

    def update_device_status(self, device_id, hub_id):
        try:
            device = HueDevice.objects.get(pk=device_id)
            hub = Hub()
            hub.set_hub(hub_id)
            
            #Get online status
            zigbee_rid = device.zigbee_rid
            if zigbee_rid:
                zigbee_item = hub.get_item('zigbee',zigbee_rid)
                if zigbee_item['status'] == 'connectivity_issue':
                    device.online = False
                elif zigbee_item['status'] == 'connected':
                    device.online = True
                device.save()
            
            #Get Power Status
            power_rid = device.power_rid
            if power_rid:
                power_item = hub.get_item('power', power_rid)
                device.battery_level =  int(power_item['power_state']['battery_level'])
                device.save()

                        
            if device.hue_device_type == 'COLORLAMP' or device.hue_device_type == 'WHITELAMP':
                #query Light model
                light_qs = HueLight.objects.get(device=device)
                light_item = hub.get_item('light',light_qs.rid)
                light_qs.light_on = bool(light_item['on']['on'])
                light_qs.dimming =  int(light_item['dimming']['brightness'])
                light_qs.effect = light_item['effects']['status']
                if device.hue_device_type == 'COLORLAMP':
                    convert = Converter(light_qs.gamut_type)
                    rgb = convert.xy_to_rgb(light_item['color']['xy']['x'], light_item['color']['xy']['y'])
                    light_qs.red = rgb[0]
                    light_qs.green = rgb[1]
                    light_qs.blue = rgb[2]
                light_qs.save()

            if device.hue_device_type == 'DIMSWITCH':
                button_qs = HueButton.objects.filter(device=device)
                for button in button_qs:
                    button_item = hub.get_item('button', button.rid)
                    button.updated = button_item['button']['button_report']['updated']
                    button.event = button_item['button']['button_report']['event']
                    button.save()

        except Exception as error:
            sys_log = SystemLogger(__name__,'update_device_status', str(error), 'ERROR')
            sys_log.log()


    def update_all_device_status(self, hub_id):
        try: 
            devices = HueDevice.objects.all()
            for device in devices:
                self.update_device_status(device.pk, hub_id)
            print('Update All Hue Complete')
        except Exception as error:
            sys_log = SystemLogger(__name__,'update_device_status', str(error), 'ERROR')
            sys_log.log()

    def sync_morph_device_types(self):
        try:
            hue_dev = HueDeviceTypes()
            dev_list = hue_dev.get_device_list()
            for dev in dev_list:
                if dev['morph_sync'] == True:
                    dev_type_qs = DeviceType.objects.filter(name=dev['morph_name'])
                    if dev_type_qs:
                        dev_type_qs[0].name = dev['morph_name']
                        dev_type_qs[0].display_name = dev['morph_display_name']
                        dev_type_qs[0].interface = 'hue'
                        dev_type_qs[0].interface_device_type = dev['hue_device_type']
                        dev_type_qs[0].capability = dev['capability']
                        dev_type_qs[0].save
                    else:
                        new_dev_type = DeviceType(
                            display_name = dev['morph_display_name'],
                            name = dev['morph_name'],
                            interface = 'hue',
                            interface_name = dev['hue_name'],
                            capability = dev['capability']
                        )
                        new_dev_type.save()         
            return 'Sync Complete'
        except Exception as error:
            sys_log = SystemLogger(__name__,'sync_morph_device_types', str(error), 'ERROR')
            sys_log.log()
            return str(error)

    def sync_morph_devices(self):
        hue_dev_types = HueDeviceTypes()
        hue_devices = HueDevice.objects.all()
        for hue_device in hue_devices:
            for hue_dev_type in hue_dev_types:
                pass
                #if hue_device.hue_device_type == 


        


        
        
        
        

        

                
                    
                    
                

            
            
            
                
        
        
        
        