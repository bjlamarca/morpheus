import os, json, threading
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .hub import Hub
from .utilities import HueUtilities
from .models import HueLight, HueDevice
from .device import light_view
from django.dispatch import receiver





current_file_directory = os.path.dirname(os.path.abspath(__file__))
result = 'None'


class HueDeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'hue-dev'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        self.my_device_id = 0
        await self.accept()
        
         

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        device_id = text_data_json['dev_id']          
        self.my_device_id = device_id
        message = await sync_to_async(light_view)(text_data)
       
        
        
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        text_data_json = json.loads(event['text'])
        if text_data_json['dev_id'] == self.my_device_id:
            message = await sync_to_async(light_view)(event['text'])
            await self.send(text_data=json.dumps(message))
        

class GenConsumer(AsyncWebsocketConsumer):
    async def connect(self):
         self.group_name = 'hue-gen'
         await self.channel_layer.group_add(self.group_name, self.channel_name)
         await self.accept()
         

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        result = 'Ok'
        if message == 'sync_device_db':
            hue = HueUtilities()
            result = await sync_to_async(hue.sync_device_db)(1)
        elif message == 'sync_morph_dev_type':
            hue = HueUtilities()
            result = await sync_to_async(hue.sync_morph_device_types)()
        elif message == 'sync_morph_dev':
            hue = HueUtilities()
            result = await sync_to_async(hue.sync_morph_devices)()
        elif message == 'update_status':
            hue = HueUtilities()
            result = await sync_to_async(hue.update_all_device_status)(1)
        

        else:
            result = "Unknown command"
        
        
        await self.channel_layer.group_send(
             self.group_name, {"type": "chat.message", "message": result}
        )

    async def chat_message(self, event):
        message = event["message"]
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
            


class DiagConsumer(AsyncWebsocketConsumer):
    async def connect(self):
         self.group_name = 'hue-diag'
         await self.channel_layer.group_add(self.group_name, self.channel_name)
         await self.accept()
         

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def get_lights(text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        hub = Hub()
        hub.set_hub(1)
        input_value = text_data_json['input_value']
        light = hub.get_light(input_value)
        print("LIGHT---", type(light))
        f = open(current_file_directory + f'/json/light-{input_value}.json', 'w')
        light_str = json.dumps(light, indent=4) 
        f.write(light_str)
        f.close
        result = light_str
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        hub = Hub()
        hub.set_hub(1)

        
        if message == 'all_lights':
            lights = hub.get_items('lights')
            f = open(current_file_directory + '/json/all_lights.json', 'w')
            lights_str = json.dumps(lights, indent=4) 
            f.write(lights_str)
            f.close
            result = lights_str

        elif message == 'all_devices':
            devices = hub.get_items('devices')
            f = open(current_file_directory + '/json/all_devices.json', 'w')
            devices_str = json.dumps(devices, indent=4) 
            f.write(devices_str)
            f.close
            result = devices_str


        elif message == 'all_buttons':
            devices = hub.get_items('buttons')
            f = open(current_file_directory + '/json/all_buttons.json', 'w')
            buttons_str = json.dumps(devices, indent=4) 
            f.write(buttons_str)
            f.close
            result = buttons_str

        elif message == 'all_zigbee':
            devices = hub.get_items('zigbee')
            f = open(current_file_directory + '/json/all_zigbee.json', 'w')
            buttons_str = json.dumps(devices, indent=4) 
            f.write(buttons_str)
            f.close
            result = buttons_str
        
        elif message == 'all_power':
            devices = hub.get_items('power')
            f = open(current_file_directory + '/json/all_power.json', 'w')
            buttons_str = json.dumps(devices, indent=4) 
            f.write(buttons_str)
            f.close
            result = buttons_str
        
        elif message == 'get_light':
            input_value = text_data_json['input_value']
            device = hub.get_item('light',input_value)
            print("device---", type(device))
            f = open(current_file_directory + f'/json/device-{input_value}.json', 'w')
            device_str = json.dumps(device, indent=4) 
            f.write(device_str)
            f.close
            result = device_str
            

        elif message == 'get_device':
            input_value = text_data_json['input_value']
            device = hub.get_item('device', input_value)
            f = open(current_file_directory + f'/json/device-{input_value}.json', 'w')
            device_str = json.dumps(device, indent=4) 
            f.write(device_str)
            f.close
            result = device_str
        
        elif message == 'get_button':
            input_value = text_data_json['input_value']
            button = hub.get_item('button', input_value)
            f = open(current_file_directory + f'/json/button-{input_value}.json', 'w')
            button_str = json.dumps(button, indent=4) 
            f.write(button_str)
            f.close
            result = button_str
        
        elif message == 'get_zigbee':
            input_value = text_data_json['input_value']
            zigbee = hub.get_item('zigbee', input_value)
            f = open(current_file_directory + f'/json/zigbee-{input_value}.json', 'w')
            button_str = json.dumps(zigbee, indent=4) 
            f.write(button_str)
            f.close
            result = button_str

        elif message == 'get_power':
            input_value = text_data_json['input_value']
            zigbee = hub.get_item('power', input_value)
            f = open(current_file_directory + f'/json/power-{input_value}.json', 'w')
            button_str = json.dumps(zigbee, indent=4) 
            f.write(button_str)
            f.close
            result = button_str

                
        elif message == 'sync_device_db':
            hue = HueUtilities()
            await sync_to_async(hue.sync_device_db)(1)
            result = 'ok'
            #result = await sync_to_async(sync_device_db)()

        elif message == 'test':
            print('hello')
            hue = HueUtilities()
            await sync_to_async(hue.update_all_device_status)(1)
            result = 'ok'


        await self.channel_layer.group_send(
             self.group_name, {"type": "chat.message", "message": result}
        )
    


    async def chat_message(self, event):
        message = event["message"]
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    
    

    

