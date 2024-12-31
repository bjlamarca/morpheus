from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import SingleTableView, MultiTableMixin
from .models import Device, Light
from .tables import DeviceTable, LightTable

def hue_main_view(request):
    return render(request, 'hue/hue.html')

def tools_view(request):
    from .models import Device
    qs = Device.objects.values_list('model_id').distinct()
    for x in qs:
        print(x)
    return render(request, 'hue/tools.html')

class DeviceListView(SingleTableView):
    model = Device
    paginate_by = 100
    table_class = DeviceTable
    template_name = 'hue/device-list.html'

class LightListView(SingleTableView):
    model = Light
    paginate_by = 100
    table_class = LightTable
    template_name = 'hue/device-list.html'

