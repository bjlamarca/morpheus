import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .scene_devices import add_remove_devices,activate_scene, delete_scene, adjust_scene

class SceneConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Sc Conn')
        await self.accept()

    async def disconnect(self, close_code):
        print('Sc Dis')
        pass

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        result = text_data_json
        print('Sc Rec', text_data_json)
        if text_data_json['type'] == 'add_remove_devices':
            result = await sync_to_async(add_remove_devices)(text_data_json['checked_id_list'], text_data_json['not_checked_id_list'], text_data_json['scene_id'] )
        if text_data_json['type'] == 'activate':
            result = await sync_to_async(activate_scene)(text_data_json['scene_id'])
        if text_data_json['type'] == 'delete':
            result = await sync_to_async(delete_scene)(text_data_json['scene_id'])
        if text_data_json['type'] == 'adjust_scene':
            result = await sync_to_async(adjust_scene)(text_data_json['scene_dev_id_list'], text_data_json['scene_parms'])
        print('Sc Res', result)
        await self.send(text_data=json.dumps(result))