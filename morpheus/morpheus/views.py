import os, json
from django.views import View
from django.shortcuts import render, HttpResponse
from utilities.logging import SystemLogger
from hue.hub import Hub
current_file_directory = os.path.dirname(os.path.abspath(__file__))

class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        hub = Hub()
        hub.set_hub(1)
        device_id = "5272447c-9bf4-4365-b7be-2404bfbac174"
        device = hub.get_items('all_lights', device_id)
        #for device in devices:
        print("DEVICE---", type(device))
        #light_str = json.dumps(lights, indent=4) 
        
        #result = light_str
        return render(request, self.template_name)
    