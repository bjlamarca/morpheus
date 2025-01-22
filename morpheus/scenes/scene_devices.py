from devices.models import Device, DeviceType
from .models import Scene, SceneDevices
from utilities.logging import SystemLogger
from devices.models import Device, Color
from devices.capabilities import get_on, get_dim, get_color, activate_device_scene
from channels.layers import get_channel_layer

logger = SystemLogger('scenes', __name__)


def add_remove_devices(checked_id_list, not_check_id_list, scene_id):  
    try:
        count_add = 0
        count_remove = 0
        scene_qs = Scene.objects.get(pk=int(scene_id))
        scene_device_qs = SceneDevices.objects.filter(scene=scene_qs)
        for dev_id in checked_id_list:
            #check if device is already in scene, if not add it
            in_scene = False
            for scene_dev in scene_device_qs:
                if int(dev_id) == scene_dev.device_id:
                    in_scene = True
            if in_scene == False:
                dev_qs = Device.objects.get(pk=int(dev_id))
                dev_type_qs = DeviceType.objects.get(device=dev_qs)
                
                new_scene_dev = SceneDevices()
                new_scene_dev.scene = scene_qs
                new_scene_dev.device = dev_qs
                new_scene_dev.scene_device_capability = dev_type_qs.capability

                if 'switch' in dev_type_qs.capability:
                    new_scene_dev.switch = get_on(dev_type_qs.interface, dev_id)
                if 'dimmer' in dev_type_qs.capability:
                    new_scene_dev.dimming = get_dim(dev_type_qs.interface, dev_id)
                if 'color' in dev_type_qs.capability:
                    rgb_list = get_color(dev_type_qs.interface, dev_id)
                    new_scene_dev.red = rgb_list[0]
                    new_scene_dev.green = rgb_list[1]
                    new_scene_dev.blue = rgb_list[2]
                        
                new_scene_dev.save()
                count_add += 1
        for dev_id in not_check_id_list:
            #check if device is already in scene, if so remove it
            in_scene = False
            for scene_dev in scene_device_qs:
                if int(dev_id) == scene_dev.device_id:
                    in_scene = True
            if in_scene == True:
                scene_dev.delete()
                count_remove += 1
        return {'type': 'add_remove_complete', 'msg_type': 'success',  'message': 'Add Remove Complete. ' + str(count_add) + ' Device(s) have been added, and ' + str(count_remove) + ' device(s) have been removed'}
        
    except Exception as error:
        logger.log('add_remove_devices','Error adding / removing devices', str(error), 'ERROR')
        return {'type': 'add_remove_complete', 'msg_type': 'error',  'message': 'Error adding and removing devices. ' + str(error)}


    



def get_avail_devices(scene_id):
    try:
    #get color, dimmers, switches - add to dict, mark ones already in scene list
        avail_devs = []
        scene_qs = Scene.objects.get(pk=scene_id)
        color_types = DeviceType.objects.filter(capability__contains='color')
        for color_type in color_types:
            color_qs = Device.objects.filter(device_type=color_type)
            for color_dev in color_qs:
                scene_dev_qs = SceneDevices.objects.filter(scene=scene_qs, device=color_dev)
                if scene_dev_qs:
                    selected = True
                else:
                    selected = False

                avail_color = {
                    'selected': selected,
                    'dev_id': color_dev.pk,
                    'dev_type': 'COLOR',
                    'dev_type_display': 'Color Lamp',
                    'dev_name': color_dev.name

                }
                avail_devs.append(avail_color)
                
        dim_types = DeviceType.objects.filter(capability__contains='dimmer').exclude(capability__contains='color')
        for dim_type in dim_types:
            dim_qs = Device.objects.filter(device_type=dim_type)
            for dim_dev in dim_qs:
                scene_dev_qs = SceneDevices.objects.filter(scene=scene_qs, device=dim_dev)
                if scene_dev_qs:
                    selected = True
                else:
                    selected = False

                avail_dim = {
                    'selected': selected,
                    'dev_id': dim_dev.pk,
                    'dev_type': 'DIMMER',
                    'dev_type_display': 'Dimmer',
                    'dev_name': dim_dev.name

                }
                avail_devs.append(avail_dim)
        switch_types = DeviceType.objects.filter(capability__contains='switch').exclude(capability__contains='color').exclude(capability__contains='dimmer')
        for switch_type in switch_types:
            switch_qs = Device.objects.filter(device_type=switch_type)
            for switch_dev in switch_qs:
                scene_dev_qs = SceneDevices.objects.filter(scene=scene_qs, device=switch_dev)
                if scene_dev_qs:
                    selected = True
                else:
                    selected = False

                avail_switch = {
                    'selected': selected,
                    'dev_id': switch_dev.pk,
                    'dev_type': 'SWITCH',
                    'dev_type_display': 'Switch',
                    'dev_name': switch_dev.name

                }
                avail_devs.append(avail_switch)

        
        return avail_devs
    except Exception as error:
        logger.log('get_avail_devices','Error getting devices', str(error), 'ERROR')

def get_device_list(scene_id):
    try:
        scene_dev_list = []
        scene_dev_qs = SceneDevices.objects.filter(scene=scene_id)
        for scene_dev in scene_dev_qs:
            capabilites = scene_dev.scene_device_capability
            if 'switch' in capabilites:
                if scene_dev.switch == 'on':
                    switch = 'On'
                elif scene_dev.switch == 'off':
                    switch  = 'Off'
                else:
                    switch = '-'
            else:
                switch = '-'
            if 'dimmer' in capabilites:
                dimming = scene_dev.dimming
            else:
                dimming = '-'
            if 'color' in capabilites:
                color = "#{:02x}{:02x}{:02x}".format(scene_dev.red, scene_dev.green, scene_dev.blue)
            else:
                color = '-'

            dev_dict = {}
            dev_dict['scene_dev_id'] = scene_dev.pk
            dev_dict['dev_name'] = scene_dev.device.name
            dev_dict['dev_type'] = scene_dev.device.device_type.display_name
            dev_dict['dev_id'] = scene_dev.device.pk
            dev_dict['switch'] = switch    
            dev_dict['dimming'] = dimming
            dev_dict['color_hex'] = color
            dev_dict['capability'] = capabilites
            dev_dict['selected'] = False
                
            
            scene_dev_list.append(dev_dict)
        return scene_dev_list
    except Exception as error:
        logger.log('get_device_list','Error getting devices', str(error), 'ERROR')




    
def activate_scene(scene_id):
    try:
        scene_qs = Scene.objects.get(pk=int(scene_id))
        scene_device_qs = SceneDevices.objects.filter(scene=scene_qs)
        scene_dict = {}
        interfaces = DeviceType.objects.values_list('interface', flat=True).distinct()
        for interface in interfaces:
            scene_dict[interface] = []
        for scene_dev in scene_device_qs:
            dev_type_qs = DeviceType.objects.get(device=scene_dev.device)
            scene_dev_dict = {}
            scene_dev_dict['device_id'] = scene_dev.device_id
            if 'switch' in dev_type_qs.capability:
                scene_dev_dict['switch'] =  scene_dev.switch
            if 'dimmer' in dev_type_qs.capability:
                scene_dev_dict['dimmer'] = scene_dev.dimming
            if 'color' in dev_type_qs.capability:
                scene_dev_dict['color']  = [scene_dev.red, scene_dev.green, scene_dev.blue]
            scene_dict[dev_type_qs.interface].append(scene_dev_dict)
        for interface in scene_dict:
            activate_device_scene(interface, scene_dict[interface])
        return {'type': 'scene_activated', 'msg_type': 'success', 'message': 'Scene has been activated'}
    except Exception as error:
        logger.log('activate_scene','Error activating Scene', str(error), 'ERROR')
        return {'type': 'scene_activated', 'msg_type': 'error', 'message': 'Error activating scene. ' + str(error)}


def delete_scene(scene_id):
    try:
        scene_qs = Scene.objects.get(pk=int(scene_id))
        scene_qs.delete()
        return {'type': 'scene_deleted', 'msg_type': 'success', 'message': 'Scene has been deleted'}
    except Exception as error:
        logger.log('delete_scene','Error deleting Scene', str(error), 'ERROR')
        return {'type': 'scene_deleted', 'msg_type': 'error', 'message': 'Error deleting scene. ' + str(error)}   

def adjust_scene(scene_dev_id_list, scene_parms):
    try:
        adj_switch = False
        adj_dim = False
        adj_color = False
        for sc_parm in scene_parms:
            if 'switch' in sc_parm:
                switch_value = sc_parm['switch']
                adj_switch = True
            
            if 'dim' in sc_parm:
                try:
                    dim_level = int(sc_parm['dim'])
                except:
                    return {'type': 'scene_adjusted', 'result': 'error', 'message': 'Dimmer level must be an number'}
                if dim_level < 0 or dim_level > 100:
                    return {'type': 'scene_adjusted', 'result': 'error', 'message': 'Dimmer level must be between 0 and 100'}
                adj_dim = True
            
            if 'color_id' in sc_parm:
                color_id = int(sc_parm['color_id'])
                if color_id == 0:
                    return {'type': 'scene_adjusted', 'result': 'error', 'message': 'Color must be selected'}
                adj_color = True
                color_qs = Color.objects.get(pk=color_id)
                red = color_qs.red
                green = color_qs.green
                blue = color_qs.blue

        for scene_dev_id in scene_dev_id_list:
            scene_dev_qs = SceneDevices.objects.get(id=int(scene_dev_id))
            dev_type_qs = DeviceType.objects.get(device=scene_dev_qs.device)
            if 'switch' in dev_type_qs.capability:
                if adj_switch:
                    scene_dev_qs.switch = switch_value
                
            if 'dimmer' in dev_type_qs.capability:
                if adj_dim:
                    scene_dev_qs.dimming = dim_level

            if 'color' in dev_type_qs.capability:
                if adj_color:
                    scene_dev_qs.red = red
                    scene_dev_qs.green = green
                    scene_dev_qs.blue = blue
            scene_dev_qs.save()
        return {'type': 'scene_adjusted', 'msg_type': 'success', 'message': 'Scene has been adjusted'}
    except Exception as error:
        logger.log('adjust_scene','Error adjusting Scene', str(error), 'ERROR')
        return {'type': 'scene_adjusted', 'msg_type': 'error', 'message': 'Error adjusting scene. ' + str(error)}  

        
