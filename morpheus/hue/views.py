from django.shortcuts import render
from django.views.generic import ListView, TemplateView, FormView
from django_tables2 import SingleTableView, MultiTableMixin
from .models import HueDevice, HueLight, HueButton
from .tables import DeviceTable, LightTable, ButtonTable

def hue_main_view(request):
    return render(request, 'hue/hue.html')

def tools_view(request):
      
    return render(request, 'hue/tools.html')

def morph_view(request, device_id):
    device = HueDevice.objects.get(pk=device_id)
    device_type = device.hue_device_type
    if device_type == 'COLORLAMP' or device_type == 'WHITELAMP':
        context = {
         'device_id': device.pk,
        }
        return render(request, 'hue/huelight.html', context=context)
    return 'Not Found'

class DeviceListView(SingleTableView):
    model = HueDevice
    paginate_by = 100
    table_class = DeviceTable
    template_name = 'hue/device-list.html'

class LightListView(SingleTableView):
    model = HueLight
    paginate_by = 100
    table_class = LightTable
    template_name = 'hue/device-list.html'

class ButtonListView(SingleTableView):
    model = HueButton
    paginate_by = 100
    table_class = ButtonTable
    template_name = 'hue/device-list.html'

class DeviceDetailView(TemplateView):
    pass


