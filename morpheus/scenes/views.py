from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from .forms import SceneForm
from .models import Scene
from .scene_devices import get_avail_devices, get_device_list

from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig
from .tables import SceneTable, SceneAddTable, SceneDeviceTable

# Create your views here.

def scene_main_view(request):
    return render(request, 'scenes/scenes.html')

def scene_create_view(request):
    print('request', request)
    scene_form = SceneForm(request.POST or None)
    context = {
        'form': scene_form,
        'post_url': reverse('scenes:create'),
        'create': 'd-none',
        
    }

    if scene_form.is_valid():
        new_scene = scene_form.save(commit=False)
        new_scene.save()
        scene_obj = Scene.objects.get(id=new_scene.pk)
        scene_form = SceneForm(request.POST or None, instance=scene_obj)
        context = {
            'form': scene_form,
            'post_url': reverse('scenes:detail', kwargs={'scene_id':scene_obj.pk}),
            'add_url': reverse('scenes:add-device', kwargs={'scene_id':scene_obj.pk}), 
            'list_url': reverse('scenes:device-list', kwargs={'scene_id':scene_obj.pk}),
            'scene_obj': scene_obj,
            'create': ''
        }
        return render(request, 'scenes/scene-detail.html', context=context)


    return render(request, 'scenes/scene-detail.html', context)


def scene_detail_view(request, scene_id):
    scene_obj = Scene.objects.get(id=scene_id)
    scene_form = SceneForm(request.POST or None, instance=scene_obj)
    context = {
        'form': scene_form,
        'post_url': reverse('scenes:detail', kwargs={'scene_id':scene_obj.pk}),
        'add_url': reverse('scenes:add-device', kwargs={'scene_id':scene_obj.pk}), 
        'dev_list_area_url': reverse('scenes:device-list-area', kwargs={'scene_id':scene_obj.pk}),
        'dev_list_url': reverse('scenes:device-list', kwargs={'scene_id':scene_obj.pk}),
        'scene_obj': scene_obj,
        'create': ''
    }
    if scene_form.is_valid():
        scene_form.save()

    return render(request, 'scenes/scene-detail.html', context=context)


def scene_add_device_view(request, scene_id):
   
    context = {
        'scene_id': scene_id,
        'list_url': reverse('scenes:add-device-list', kwargs={'scene_id':scene_id}),
        
    }
    
    return render(request, 'scenes/scene-device-add.html', context)

def scene_add_device_list_view(request, scene_id):
    avail_dict = get_avail_devices(scene_id)
    table = SceneAddTable(avail_dict)
    RequestConfig(request, paginate=False).configure(table)
    context = {
        'scene_id': scene_id,
        'table': table
    }
    
    return render(request, 'scenes/scene-add-dev-list.html', context)

def scene_device_list_area_view(request, scene_id):
    context = {
        'scene_id': scene_id,
        'dev_list_url': reverse('scenes:device-list', kwargs={'scene_id':scene_id}),
    }
    return render(request, 'scenes/scene-dev-list-area.html', context)

def scene_device_list_view(request, scene_id):
    dev_list = get_device_list(scene_id)
    table = SceneDeviceTable(dev_list)
    RequestConfig(request, paginate=False).configure(table)
    context = {
        'scene_id': scene_id,
        'table': table
    }
    return render(request, 'scenes/scene-dev-list.html', context)

def scene_adjust_view(request):
    return render(request, 'scenes/scene-adjust.html')



class SceneListView(SingleTableView):
    model = Scene
    paginate_by = 100
    table_class = SceneTable
    template_name = 'scenes/scene-list.html'


# class SceneAddDevListView(TemplateView, SingleTableMixin):
#     template_name = 'scenes/scene-list.html'
#     table_class = SceneAddTable
#     print('TYPE', type(get_avail_devices(1)))
#     table_data = get_avail_devices(1)

    


