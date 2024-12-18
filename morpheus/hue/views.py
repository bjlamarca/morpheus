from django.shortcuts import render
from django.views.generic import ListView
from .models import Device

def hue_main_view(request):
    return render(request, 'hue/hue.html')

def tools_view(request):
    from .models import Device
    qs = Device.objects.values_list('model_id').distinct()
    for x in qs:
        print(x)
    return render(request, 'hue/tools.html')

class DeviceListView(ListView):
    model = Device
    template_name = 'hue/hue.html'
