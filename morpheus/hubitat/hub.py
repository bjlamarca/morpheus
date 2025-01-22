
import requests
import json

class Hubitat():
    def __init__(self):
        self.hub_id = ''
        self.hub_name = ''
        self.url_pre = ''
        self.url_post = ''

    def set_hub(self, hub_id):
        if hub_id == 1:
            self.hub_name = 'PC'
            ip_addr = '192.168.55.5'
            access_token = '970d2274-9857-4268-81a6-8b37b1ab569e'
            device_id = '614'
        self.url_pre = f'http://{ip_addr}/apps/api/{device_id}/'
        self.url_post = f'?access_token={access_token}'
    
    def get_all_devices(self):
        url = self.url_pre + 'devices' + self.url_post
        result = requests.get(url, verify=False)
        result_json = json.loads(result.text)
        for device in result_json:
            print(device, type(device))

    def get_device(self, device_id):
        url = self.url_pre + 'devices/' + device_id + self.url_post
        result = requests.get(url, verify=False)
        result_json = json.loads(result.text)
        print(json.dumps(result_json, indent=4))

    def get_device_commands(self, device_id):
        url = self.url_pre + 'devices/' + device_id + '/commands' + self.url_post
        result = requests.get(url, verify=False)
        result_json = json.loads(result.text)
        print(json.dumps(result_json, indent=4))

    def get_device_capabilities(self, device_id):
        url = self.url_pre + 'devices/' + device_id + '/capabilities' + self.url_post
        result = requests.get(url, verify=False)
        result_json = json.loads(result.text)
        print(json.dumps(result_json, indent=4))
        