from django.shortcuts import render
from django.urls import reverse
from .forms import PageForm
from .models import Page
from django_tables2 import SingleTableView
from .tables import PageTable 


def home_view(request):
    return render(request, 'tiles/tiles-home.html')

def page_create_view(request):
    print('page_create_view', request.POST)
    page_form = PageForm(request.POST or None)
    context = {
        'form': page_form,
        'post_url': reverse('tiles:create'),
        'sub_class': 'd-none',
        'form_type': 'create'
        
    }

    if page_form.is_valid():
        print('valid')
        new_page = page_form.save(commit=False)
        new_page.save()
        page_obj = Page.objects.get(id=new_page.pk)
        page_form = PageForm(request.POST or None, instance=page_obj)
        context = {
            'form': page_form,
            'post_url': reverse('tiles:detail', kwargs={'page_id':page_obj.pk}),
            'page_obj': page_obj,
            'sub_class': '',
            'form_type': 'edit',
            'page_id': page_obj.pk
        }
        return render(request, 'tiles/tiles-page-detail.html', context=context)

    return render(request, 'tiles/tiles-page-detail.html', context=context)

def page_detail_view(request, page_id):
    page_obj = Page.objects.get(id=page_id)
    page_form = PageForm(request.POST or None, instance=page_obj)
    context = {
        'form': page_form,
        'post_url': reverse('tiles:detail', kwargs={'page_id':page_obj.pk}),
        'page_obj': page_obj,
        'sub_class': '',
        'form_type': 'edit',
        'page_id': page_obj.pk
    }
    if page_form.is_valid():
        page_form.save()

    return render(request, 'tiles/tiles-page-detail.html', context=context)


class PageListView(SingleTableView):
    model = Page
    paginate_by = 100
    table_class = PageTable
    template_name = 'tiles/tiles-page-list.html'
    
    


def tiles_main_view(request):
    return render(request, 'tiles/tiles-main.html')

def scene_tile_view(request):
    return render(request, 'tiles/scene-tile.html')

def nav_tile_view(request):
    return render(request, 'tiles/nav-tile.html')

def tile_page_view(request):
    
    tiles = []
    for i in range(15):
        tiles.append({
            'name': 'Tile ' + str(i),
            'number': str(i),
            'url': reverse('tiles:scene-tile'),
            }
        )
    
    tiles.append({
            'name': 'Tile ' + str(20),
            'number': str(20),
            'url': reverse('tiles:nav-tile'),
            }
        )

    context = {
        'tiles': tiles
    }

    return render(request, 'tiles/page-tile.html', context=context)



def pages_view(request):
    return render(request, 'tiles/tiles-pages.html')


#reverse('scenes:device-list', kwargs={'scene_id':scene_obj.pk}),