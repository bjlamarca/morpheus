import os, json, threading
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .hub import Hub
from .database import sync_device_db



current_file_directory = os.path.dirname(os.path.abspath(__file__))
result = 'None'

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
            lights = hub.get_all_lights()
            f = open(current_file_directory + '/json/all_lights.json', 'w')
            lights_str = json.dumps(lights, indent=4) 
            f.write(lights_str)
            f.close
            result = lights_str

        elif message == 'all_devices':
            devices = hub.get_all_devices()
            f = open(current_file_directory + '/json/all_devices.json', 'w')
            devices_str = json.dumps(devices, indent=4) 
            f.write(devices_str)
            f.close
            result = devices_str


        elif message == 'all_buttons':
            devices = hub.get_all_buttons()
            f = open(current_file_directory + '/json/all_buttons.json', 'w')
            buttons_str = json.dumps(devices, indent=4) 
            f.write(buttons_str)
            f.close
            result = buttons_str
        
        elif message == 'get_light':
            t = threading.Thread(target=self.get_lights())
            t.daemon = True
            t.start()
            

        elif message == 'get_device':
            input_value = text_data_json['input_value']
            device = hub.get_device(input_value)
            print("device---", type(device))
            f = open(current_file_directory + f'/json/device-{input_value}.json', 'w')
            device_str = json.dumps(device, indent=4) 
            f.write(device_str)
            f.close
            result = device_str
        
        elif message == 'get_button':
            input_value = text_data_json['input_value']
            button = hub.get_button(input_value)
            f = open(current_file_directory + f'/json/button-{input_value}.json', 'w')
            button_str = json.dumps(button, indent=4) 
            f.write(button_str)
            f.close
            result = button_str
        
        elif message == 'sync_device_db':
            result = await sync_to_async(sync_device_db)()

        elif message == 'test':
            
            result = 'Good'


        await self.channel_layer.group_send(
             self.group_name, {"type": "chat.message", "message": result}
        )
    


    async def chat_message(self, event):
        message = event["message"]
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    
    

    

