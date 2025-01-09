from django.shortcuts import render
from importlib import import_module
from .models import Device, DeviceType
from django_tables2 import SingleTableView
from .tables import DeviceTable

# Create your views here.


def devices_main_view(request):
    return render(request, 'devices/devices.html')


class DeviceListView(SingleTableView):
    model = Device
    paginate_by = 100
    table_class = DeviceTable
    template_name = 'hue/device-list.html'

def device_detail_view(request, device_id):
    device = Device.objects.get(pk=device_id)
    interface = device.device_content_type.app_label
    interface_view = import_module(interface + '.' + 'views')
    morph_view = interface_view.morph_view
    #print(morph_view(request, device.device_object_id))
    
    return morph_view(request, device.device_object_id)

