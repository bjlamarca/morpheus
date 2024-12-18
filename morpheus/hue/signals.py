from django.dispatch import Signal
from django.dispatch import receiver
import json

hue_receive = Signal()

@receiver(hue_receive)
def receive_hue_data(sender, **kwargs):
    data = json.dumps(kwargs['data'], indent=2)
    #result = next(iter(data))
    #print("Sender", data, '\n')
