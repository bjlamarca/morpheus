from asgiref.sync import sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .tiles import delete_page




class TileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'tile-gen'
        print('Tile Conn')
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print('Tile Dis')
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass
        text_data_json = json.loads(text_data)
        print('Tile Rec', text_data_json)
        result = {'type': 'no data'}
        if text_data_json['type'] == 'delete_page':
            result = await sync_to_async(delete_page)(text_data_json['page_id'])
          

        await self.send(text_data=json.dumps(result))



    async def chat_message(self, event):
        message = event["message"]
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

class TileUIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Tile Conn')
        await self.accept()

    async def disconnect(self, close_code):
        print('Tile Dis')
        pass

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        print('Tile Rec', text_data_json)
        #message = await sync_to_async(activate_scene)(29)
        #activate_scene(29)

        #await self.send(text_data=json.dumps(text_data_json))