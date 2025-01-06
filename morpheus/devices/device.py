from importlib import import_module

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
