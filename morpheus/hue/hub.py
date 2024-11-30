import threading, requests, json , httpx
from pprint import pprint
from django.dispatch import receiver
from .signals import hue_receive
from utilities.logging import SystemLogger


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

    #Function to get info from the hub
    def get_items(self, item, device_id=None):
        if item == 'all_lights':
            url = self.url_pre + '/clip/v2/resource/light'
        elif item == 'all_devices':
            url = self.url_pre + '/clip/v2/resource/device'
        elif item == 'device':
            url = self.url_pre + '/clip/v2/resource/device/' + device_id
        elif item == 'light':
            url = self.url_pre + '/clip/v2/resource/light/' + device_id
        else:
            sys_log = SystemLogger('Hue Hub', 'Get All Devices','Not a vaild Item(s)', 'ERROR')
            sys_log.log()
            return None
        try:
            result = requests.get(url, headers=self.header, verify=False)
            return_dict = dict(json.loads(result.text))
            errors_list = return_dict['errors']
            print("Error", errors_list)
            if bool(errors_list):
                sys_log = SystemLogger('Hue Hub','Cannot retrieve data from Hub', errors_list, 'ERROR')
                sys_log.log()
                return None
            else:
                print('TYPE')
                data_list = return_dict['data']
                return data_list
            

        except Exception as error:
            pass     
    
    
    def get_device(self, device_id):
        url = self.url_pre + '/clip/v2/resource/device/' + device_id
        result = requests.get(url, headers=self.header, verify=False)
        result_dict = json.loads(result.text)
        device_list = result_dict['data']
        device_dict = dict(device_list[0]) 
        return(device_dict)
    
    
    
    def get_all_buttons(self):
        url = self.url_pre + '/clip/v2/resource/button'
        result = requests.get(url, headers=self.header, verify=False)
        button_dict = json.loads(result.text)
        button_list = button_dict['data'] 
        return button_list
    
    def get_light(self, light_id):
        self.url = self.url_pre + '/clip/v2/resource/light/' + light_id
        result = self.get_from_hub()
        print("RESULT", result, type(result) )
        
        #light_dict = dict(light_list[0]) 
        return(result)
    
    def get_button(self, button_id):
        url = self.url_pre + '/clip/v2/resource/button/' + button_id
        result = requests.get(url, headers=self.header, verify=False)
        result_dict = json.loads(result.text)
        button_list = result_dict['data']
        button_dict = dict(button_list[0]) 
        return button_dict
    
    
    ###Functions to control devices
    def light_control(self, light_id, data):
        url = self.url_pre + '/clip/v2/resource/light/' + light_id
        
        result = requests.put(url, data=data, headers=self.header, verify=False)
        print(result.text)

      

    #System for processing messages from Hub
    def get_stream(self):
        url = self.url_pre + '/eventstream/clip/v2'
        with httpx.stream('GET', url, headers=self.header, verify=False, timeout=None) as s:
            for data in s.iter_text():
                #print("d1",data)
                yield data
                #yield s.iter_text()

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
        try:
            event_dict = json.loads(hue_data)
            hue_receive.send(sender='hue_process_events', data=event_dict)
            #pprint(event_dict)
        except Exception as error:
            print("Hue Receive Error:", error)

        
        
    


def list_lights(device_list):
    for device in device_list:
        for service in device['services']:
            if service['rtype'] == 'light':
                print(device['metadata']['name'], service['rid'], device['product_data']['product_name'], device['product_data']['model_id'])




   
