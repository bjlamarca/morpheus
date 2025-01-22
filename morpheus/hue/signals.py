from django.dispatch import Signal, receiver
import json
from utilities.logging import SystemLogger
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = SystemLogger('hue', __name__)
device_update = Signal()



hue_device_signal = Signal()
@receiver(hue_device_signal)
def handle_device_signal(sender, **kwargs):
    try:
        data = kwargs.get('data') 
        if data['type'] == 'update':
            device_id = str(data['device_id'])
            send_dict = json.dumps({'type': 'update', 'dev_id': device_id})
            

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('hue-dev', {"type": "chat.message", "text": send_dict,}, )
    except Exception as error:
        logger.log('handle_device_signal','Error handling signal', error, 'ERROR')
