import threading, requests, json , httpx
from pprint import pprint
from django.dispatch import receiver
from .signals import hue_receive
from utilities.logging import SystemLogger
from pprint import pprint



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
            url = self.url_pre + '/clip/v2/resource/button.' + device_id
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

      

    #System for processing messages from Hub
    def get_stream(self):
        url = self.url_pre + '/eventstream/clip/v2'
        with httpx.stream('GET', url, headers=self.header, verify=False, timeout=None) as s:
            s.read()
            yield s.text
            #for data in s.iter_text():
                
            #     #print("d1",data)
            #    yield data
            #     #yield s.iter_text()

    def loop_stream(self):
        while True:
            result = self.get_stream()
            for data in result:
                self.hue_process_events(data) 
            #time.sleep(.1)


    def hue_receive_events(self):
        print("Start Hue")
        t = threading.Thread(target=self.loop_stream)
        t.daemon = True
        t.start()
    
    def hue_process_events(self, hue_data):
        #refer to hueupdates.md
        #try:
            event_list = json.loads(hue_data)
            for event_dict in event_list:
                print(event_dict['creationtime'])
                for data_item in event_dict['data']:
                    update_type = data_item['type']
                    print('DATA ITEM', update_type)
                    if update_type == 'light':
                        if 'on' in data_item:
                            print('on:', data_item['on'] )
                        if 'dimming' in data_item:
                            print('Dim:', data_item['dimming'])
                        if 'color' in data_item:
                            print('color:', data_item['color'])
                    elif update_type == 'zigbee_connectivity':
                        if 'status' in data_item:
                            print(data_item['status'])
                    elif update_type == 'device_power':
                        if 'power_state' in data_item:
                            print(data_item['power_state'])
                    elif update_type == 'button':
                        print(data_item)

                    





        #except Exception as error:
            #print("Hue Receive Error:", error)



def list_lights(device_list):
    for device in device_list:
        for service in device['services']:
            if service['rtype'] == 'light':
                print(device['metadata']['name'], service['rid'], device['product_data']['product_name'], device['product_data']['model_id'])




   
