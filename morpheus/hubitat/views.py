from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def hubitat_receive_view(request):
    data_bytes  = request.body
    data = data_bytes.decode('utf-8')
    data_dict = json.loads(data)
    f = open('logs/hubitatlog.json', 'a')
    time = str(datetime.now())
    data_json = json.dumps(data_dict, indent=2) 
    f.write(time + ' ' + data_json + ',\n')
    f.close
    return HttpResponse('OK', status=200)
