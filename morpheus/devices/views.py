from django.shortcuts import render
from importlib import import_module
from .models import Device, DeviceType, Color
from django_tables2 import SingleTableView, RequestConfig
from .tables import DeviceTable, DeviceColorTable
from .color import get_color_list

# Create your views here.


def devices_main_view(request):
    return render(request, 'devices/devices.html')

def device_color_view(request):
    table = DeviceColorTable(Color.objects.all().order_by('sort'))
    RequestConfig(request, paginate=False).configure(table)
    context = {
        'table': table
    }
    return render(request, 'devices/device-color.html', context)


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

def device_colorpicker_view(request):
    colors = Color.objects.filter(favorite=True).order_by('sort')
    for color in colors:
        print(color)
    context = {
        'colors': colors
    }
    
    return render(request, 'devices/device-colorpicker.html', context)

