from importlib import import_module
from .models import Color

DEVICE_TYPES = [
    {
    'name': 'Hue White Lamp',
    'interface': 'hue'
     }
]

def import_test():
    module = import_module('hue.device')
    thisClass = getattr(module, 'Capability')
    instance = thisClass()
    instance.On(True)


def update_color_favorite(color_id, checked):
    color = Color.objects.get(pk=color_id)
    color.favorite = checked
    color.save()
    
