import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .scene_devices import add_remove_devices,activate_scene

class SceneConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Sc Conn')
        await self.accept()

    async def disconnect(self, close_code):
        print('Sc Dis')
        pass

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'add_remove_devices':
            text_data_json = await sync_to_async(add_remove_devices)(text_data_json['checked_id_list'], text_data_json['not_checked_id_list'], text_data_json['scene_id'] )
        if text_data_json['type'] == 'activate':
            text_data_json = await sync_to_async(activate_scene)(text_data_json['scene_id'])
            
        await self.send(text_data=json.dumps(text_data_json))