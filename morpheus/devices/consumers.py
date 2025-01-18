import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .device import update_color_favorite

class GenConsumer(AsyncWebsocketConsumer):
    async def connect(self):
         self.group_name = 'dev-gen'
         await self.channel_layer.group_add(self.group_name, self.channel_name)
         await self.accept()
         

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        #message = text_data_json['message']
        #print('msg', message)
        result = 'Ok'
        if text_data_json['type'] == 'color_favorite':
            text_data_json = await sync_to_async(update_color_favorite)(text_data_json['color_id'], text_data_json['checked'] )
            result = 'Color Favorite Updated'
        
        await self.send(text_data=json.dumps({"message": result}))
        # await self.channel_layer.group_send(
        #      self.group_name, {"type": "chat.message", "message": result}
        # )

    async def chat_message(self, event):
        message = event["message"]
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))