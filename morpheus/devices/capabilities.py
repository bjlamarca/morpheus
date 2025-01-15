from importlib import import_module

CAPABILITY = [
    'switch',
    'dimmer',
    'color',


]


def switch(interface, device_id, state):
    module = import_module(interface + '.capabilities')
    thisClass = getattr(module, 'Capabilities')
    instance = thisClass()
    instance.switch(device_id, state)

def dimmer(interface, device_id, dim_level):
    module = import_module(interface + '.capabilities')
    thisClass = getattr(module, 'Capabilities')
    instance = thisClass()
    instance.dimmer(device_id, dim_level)

def color(interface, device_id, red, green, blue):
    module = import_module(interface + '.capabilities')
    thisClass = getattr(module, 'Capabilities')
    instance = thisClass()
    instance.color(device_id, red, green, blue)

def activate_device_scene(interface, scene_dev_list):
    module = import_module(interface + '.capabilities')
    thisClass = getattr(module, 'Capabilities')
    instance = thisClass()
    instance.activate_scene(scene_dev_list)

def get_on(interface, device_id):
    module = import_module(interface + '.capabilities')
    thisClass = getattr(module, 'Capabilities')
    instance = thisClass()
    return instance.get_on(device_id)

def get_dim(interface, device_id):
    module = import_module(interface + '.capabilities')
    thisClass = getattr(module, 'Capabilities')
    instance = thisClass()
    return instance.get_dim(device_id)

def get_color(interface, device_id):
    module = import_module(interface + '.capabilities')
    thisClass = getattr(module, 'Capabilities')
    instance = thisClass()
    return instance.get_color(device_id)

