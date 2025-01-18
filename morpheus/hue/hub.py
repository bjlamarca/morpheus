import threading, requests, json , httpx
from pprint import pprint
from django.dispatch import receiver
from .signals import hue_device_signal
from utilities.logging import SystemLogger
from .models import HueDevice, HueLight, HueButton
from .color import Converter
from django.contrib.auth.models import User




class Hub():
    def __init__(self) -> None:
        self.hub_name = ''
        self.username = ''
        self.hub_ip = ''
        self.url_pre = ''
        self.url = ''
        self.header = ''
        self.hub_id = 0
      
    def set_hub(self, hub_id):
        self.hub_id = hub_id
        match self.hub_id:
            case 2:
                self.username = '63MXXAB8g2X5aof6R3wBjgFJyARx5zA1K3QKjCUe'
                self.hub_ip = '192.168.57.230'
                CLIENTKEY = 'C2E4482048D10998FE4AB655C28201B4'
                self.hub_name = 'Goose'
            case 1:
                self.username ='zS-Ja5QNFWr8CKKLnLv2It9qTQ6m0SvwA2s6nFJi'
                self.hub_ip = '192.168.55.12'
                CLIENTKEY = '2DCE7A4AF2D0E44AA77CC11A0CF6D850'
                self.hub_name = 'PC'
                

        self.url_pre = "https://" + self.hub_ip
        self.header = {"hue-application-key": self.username}
        
    
    def generate_key(self):
        url = self.url_pre + '/api'
        data = '{"devicetype":"app_name#instance_name", "generateclientkey":true}'
        result = requests.post(url=url, data=data, verify=False)
        return result.text

    #Get items from the hub, return a list of dicts
    def get_items(self, item):
        if item == 'lights':
            url = self.url_pre + '/clip/v2/resource/light'
        elif item == 'devices':
            url = self.url_pre + '/clip/v2/resource/device'
        elif item == 'buttons':
            url = self.url_pre + '/clip/v2/resource/button'
        elif item == 'zigbee':
            url = self.url_pre + '/clip/v2/resource/zigbee_connectivity'
        elif item == 'power':
            url = self.url_pre + '/clip/v2/resource/device_power'
        
        else:
            sys_log = SystemLogger('Hue Hub', 'Get Items','Not vaild Item(s)', 'ERROR')
            sys_log.log()
            return None
        try:
            result = requests.get(url, headers=self.header, verify=False)
            return_dict = dict(json.loads(result.text))
            errors_list = return_dict['errors']
            if bool(errors_list):
                sys_log = SystemLogger('Hue Hub','Hub returned Errors attempting to get Items', errors_list, 'ERROR')
                sys_log.log()
                return None
            else:
                data_list = return_dict['data']
                return data_list
        except Exception as error:
            sys_log = SystemLogger('Hue Hub','Cannot retrieve items from Hub.', str(error), 'ERROR')
            sys_log.log()
            return None

    #Get an item from the hub, returns a dict
    def get_item(self, item, device_id=None):
        if item == 'device':
            url = self.url_pre + '/clip/v2/resource/device/' + device_id
        elif item == 'light':
            url = self.url_pre + '/clip/v2/resource/light/' + device_id
        elif item == 'button':
            url = self.url_pre + '/clip/v2/resource/button/' + device_id
        elif item == 'zigbee':
            url = self.url_pre + '/clip/v2/resource/zigbee_connectivity/' + device_id
        elif item == 'power':
            url = self.url_pre + '/clip/v2/resource/device_power/' + device_id
        else:
            sys_log = SystemLogger('Hue Hub', 'Get All Devices','Not a vaild Item(s)', 'ERROR')
            sys_log.log()
            return None
        try:
            result = requests.get(url, headers=self.header, verify=False)
            return_dict = dict(json.loads(result.text))
            errors_list = return_dict['errors']
            if bool(errors_list):
                sys_log = SystemLogger('Hue Hub','Cannot retrieve data from Hub', errors_list, 'ERROR')
                sys_log.log()
                return None
            else:
                data_list = return_dict['data']
                #return first (only) item from list as a dict
                return dict(data_list[0])
        except Exception as error:
            sys_log = SystemLogger('Hue Hub','Cannot retrieve item from Hub.', error, 'ERROR')
            sys_log.log()
            return None         
    
    
    ###Functions to control devices
    def light_control(self, light_id, data):
        url = self.url_pre + '/clip/v2/resource/light/' + light_id
        
        result = requests.put(url, data=data, headers=self.header, verify=False)
        print(result.text)
        return result

    def light_set_on(self, state, light_id):
            #State is string, 'on' or 'off'
            #light is pk from Light Model
            light_qs = HueLight.objects.get(pk=light_id)
            url = self.url_pre + '/clip/v2/resource/light/' + light_qs.rid
            if state == 'on':
                 data = '{"on": {"on": true}}'
            elif state == 'off':
                 data = '{"on": {"on": false}}'
            result = requests.put(url, data=data, headers=self.header, verify=False)
            print(result)

    def light_set_dimming(self, dim_level, light_id):
            #light is pk from Light Model
            light_qs = HueLight.objects.get(pk=light_id)
            url = self.url_pre + '/clip/v2/resource/light/' + light_qs.rid
            data = '{"dimming":{"brightness":' + str(dim_level) + '}}'
            result = requests.put(url, data=data, headers=self.header, verify=False)
            print(result)

    def light_set_color(self, red, green, blue, light_id):
        light_qs = HueLight.objects.get(pk=light_id)
        url = self.url_pre + '/clip/v2/resource/light/' + light_qs.rid
        convert = Converter(light_qs.gamut_type)
        xy = convert.rgb_to_xy(red, green, blue)
        data = '{"color":{"xy":{"x":' + str(xy[0]) + ',"y":' + str(xy[1]) + '}}}'
        result = requests.put(url, data=data, headers=self.header, verify=False)
        print(result)

    def light_set_color_dim_on(self, red, green, blue, dim_level, on_state, light_id):
        light_qs = HueLight.objects.get(pk=light_id)
        url = self.url_pre + '/clip/v2/resource/light/' + light_qs.rid
        convert = Converter(light_qs.gamut_type)
        xy = convert.rgb_to_xy(red, green, blue)
        if on_state == 'on':
            on_data = '"on": {"on": true}'
        elif on_state == 'off':
            on_data = '"on": {"on": false}'
        data = '{"color":{"xy":{"x":' + str(xy[0]) + ',"y":' + str(xy[1]) + '}}, "dimming":{"brightness":' + str(dim_level) + '},' + on_data + '}'
        result = requests.put(url, data=data, headers=self.header, verify=False)
        print(result)

    def light_set_dim_on(self, dim_level, on_state, light_id):
        light_qs = HueLight.objects.get(pk=light_id)
        url = self.url_pre + '/clip/v2/resource/light/' + light_qs.rid
        if on_state == 'on':
            on_data = '"on": {"on": true}'
        elif on_state == 'off':
            on_data = '"on": {"on": false}'
        data = '{"dimming":{"brightness":' + str(dim_level) + '},' + on_data + '}'
        result = requests.put(url, data=data, headers=self.header, verify=False)
        print(result)

    

        

    #System for processing messages from Hub
    def get_stream(self):
        url = self.url_pre + '/eventstream/clip/v2'
        with httpx.stream('GET', url, headers=self.header, verify=False, timeout=None) as s:
            s.read()
            yield s.text
            

    def loop_stream(self):
        while True:
            result = self.get_stream()
            for data in result:
                self.hue_process_events(data) 
           

    def hue_receive_events(self):
        print("Start Hue")
        t = threading.Thread(target=self.loop_stream)
        t.daemon = True
        t.start()
    
    def hue_process_events(self, hue_data):
        #refer to hueupdates.md
        try:
            event_list = json.loads(hue_data)
            for event_dict in event_list:
                
                for data_item in event_dict['data']:
                    update_type = data_item['type']
                    hue_signal = {}
                    hue_signal['type'] = 'update'
                    hue_signal['update_type'] = update_type
                    if update_type == 'light':
                        device_qs = HueDevice.objects.get(hue_id=data_item['owner']['rid'])
                        light_qs = HueLight.objects.get(rid=data_item['id'])
                        hue_signal['device_id'] = device_qs.pk
                        hue_signal['light_id'] = light_qs.pk
                        if 'on' in data_item:
                            if data_item['on']['on'] == True:
                                light_qs.switch = 'on'
                                hue_signal['switch'] = 'on'
                            elif data_item['on']['on'] == False:
                                light_qs.switch = 'off'
                                hue_signal['switch'] = 'off'
                            hue_signal['light_on'] = data_item['on']['on']
                        if 'dimming' in data_item:
                            light_qs.dimming =  int(data_item['dimming']['brightness'])
                            hue_signal['dimming'] = int(data_item['dimming']['brightness'])
                        if 'color' in data_item:
                            convert = Converter(light_qs.gamut_type)
                            rgb = convert.xy_to_rgb(data_item['color']['xy']['x'], data_item['color']['xy']['y'])
                            light_qs.red = rgb[0]
                            light_qs.green = rgb[1]
                            light_qs.blue = rgb[2]
                            hue_signal['red'] = rgb[0]
                            hue_signal['green'] = rgb[1]
                            hue_signal['blue'] = rgb[0]
                        light_qs.save()
                        hue_device_signal.send(sender='hue_process_events', data=hue_signal)

                    elif update_type == 'zigbee_connectivity':
                        device_qs = HueDevice.objects.get(hue_id=data_item['owner']['rid'])
                        if 'status' in data_item:
                            if data_item['status'] == 'connectivity_issue':
                                device_qs.online = False
                            elif data_item['status'] == 'connected':
                                device_qs.online = True
                            device_qs.save()
                    elif update_type == 'device_power':
                        device_qs = HueDevice.objects.get(hue_id=data_item['owner']['rid'])
                        if 'power_state' in data_item:
                            device_qs.battery_level =  int(data_item['power_state']['battery_level'])
                            device_qs.save()
                    elif update_type == 'button':
                        device_qs = HueDevice.objects.get(hue_id=data_item['owner']['rid'])
                        button_qs = HueButton.objects.get(rid=data_item['id'])
                        button_qs.updated = data_item['button']['button_report']['updated']
                        button_qs.event = data_item['button']['button_report']['event']
                        button_qs.save()
                    elif update_type == 'grouped_light':
                        pass
                    elif update_type == 'geolocation':
                        pass
                    elif update_type == 'scene':
                        pass
                    else:
                        sys_log = SystemLogger(__name__,'hue_process_events', update_type + ' is an unknow device type', 'WARNING')
                        sys_log.log()

                        

                    
        except Exception as error:
            sys_log = SystemLogger(__name__,'hue_process_events', str(error), 'ERROR')
            sys_log.log()

        


              

def list_lights(device_list):
    for device in device_list:
        for service in device['services']:
            if service['rtype'] == 'light':
                print(device['metadata']['name'], service['rid'], device['product_data']['product_name'], device['product_data']['model_id'])




   
