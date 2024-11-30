from django.dispatch import Signal
from django.dispatch import receiver

hue_receive = Signal()

@receiver(hue_receive)
def receive_hue_data(sender, **kwargs):
    print("Sender", kwargs['data'], '\n')
