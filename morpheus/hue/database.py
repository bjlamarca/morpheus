import json
from hue.hub import Hub
from .models import Device
from .devices import HueDevice

hub_id = 1

def sync_device_db():
    
    
    
    hub = Hub()
    hub.set_hub(hub_id)
    devices = hub.get_all_devices()
    
    
    for device in devices:
        print('Type', type(device) )
        
        
        device_model = Device.objects.filter(hue_id=device['id'])
        if device_model:
            print('Device found, update it')
            pass
        else:
            print('Device not found, create it')
            device_model = HueDevice()
            device_model.device_dict = device
            device_model.hub_id = hub_id
            
                        
            device_model.add_device()
            
            
        
        #print(device['product_data']['product_name'], device['product_data']['model_id'], device['metadata']['name'])
        
    
    return json.dumps(devices, indent=2)