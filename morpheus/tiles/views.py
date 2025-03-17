from django.shortcuts import render
from django.urls import reverse
from .forms import PageForm, SectionForm, TileForm
from .models import Page, PageSection, Tile
from django_tables2 import SingleTableView, RequestConfig
from .tables import PageTable, PageSectionTable, TileTable


def admin_view(request):
    return render(request, 'tiles/tiles-home.html')

def page_main_view(request):
    return render(request, 'tiles/tiles-pages.html')


class PageListView(SingleTableView):
    model = Page
    paginate_by = 100
    table_class = PageTable
    template_name = 'tiles/tiles-page-list.html'

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
            'add_section_url': reverse('tiles:section-create', kwargs={'page_id':page_obj.pk}),
            'section_list_url': reverse('tiles:section-list', kwargs={'page_id':page_obj.pk}),
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
        'add_section_url': reverse('tiles:section-create', kwargs={'page_id':page_obj.pk}),
        'section_list_url': reverse('tiles:section-list', kwargs={'page_id':page_obj.pk}),
        'page_obj': page_obj,
        'sub_class': '',
        'form_type': 'edit',
        'page_id': page_obj.pk
    }
    if page_form.is_valid():
        page_form.save()

    return render(request, 'tiles/tiles-page-detail.html', context=context)

def section_create_view(request, page_id):
    page_obj = Page.objects.get(pk=page_id)
    section_form = SectionForm(request.POST or None, page_obj=page_obj)
    context = {
        'page_obj': page_obj,
        'post_url': reverse('tiles:section-create', kwargs={'page_id':page_id}),
        'form': section_form,
        'form_type': 'create',
    }
    
    if section_form.is_valid():
        section_obj = section_form.save()
        section_form = SectionForm(request.POST or None, page_obj=page_obj)
        context = {
            'page_obj': page_obj,
            'post_url': reverse('tiles:section-detail', kwargs={'section_id':section_obj.pk}),
            'form': section_form,
            'section_obj': section_obj,
            'form_type': 'edit',
        }
        return render(request, 'tiles/tiles-section.html', context=context)

    return render(request, 'tiles/tiles-section.html', context=context)

def section_detail_view(request, section_id):
    section_obj = PageSection.objects.get(pk=section_id)
    section_form = SectionForm(request.POST or None, instance=section_obj)
    context = {
        'page_obj': section_obj.page,
        'post_url': reverse('tiles:section-detail', kwargs={'section_id':section_obj.pk}),
        'form': section_form,
        'section_obj': section_obj,
        'form_type': 'edit',
        'ub_class': '',
        'add_tile_url': reverse('tiles:tile-create', kwargs={'section_id':section_obj.pk}),
        'tile_list_url': reverse('tiles:tile-list', kwargs={'section_id':section_obj.pk}),
    }
    
    if section_form.is_valid():
        section_form.save()
        
    return render(request, 'tiles/tiles-section.html', context=context)

def section_list_view(request, page_id):
    page_obj = Page.objects.get(pk=page_id)
    sections = PageSection.objects.filter(page=page_obj)
    table = PageSectionTable(sections)
    RequestConfig(request, paginate=False).configure(table)
    
    context = {
        'table': table,
        
    }
    return render(request, 'tiles/tiles-section-list.html', context=context)

def tiles_list_view(request, section_id):
    section_obj = PageSection.objects.get(pk=section_id)
    tiles = Tile.objects.filter(page_section=section_obj)
    table = TileTable(tiles)
    RequestConfig(request, paginate=False).configure(table)
    context = {
        'table': table,
        'section_obj': section_obj,
    }
    return render(request, 'tiles/tiles-tile-list.html', context=context)
    

def tile_detail_view(request, tile_id):
    tile_obj = Tile.objects.get(pk=tile_id)
    tile_form = TileForm(request.POST or None, instance=tile_obj)
    print('tile_obj', tile_obj)
    context = {
        'tile_obj': tile_obj,
        'post_url': reverse('tiles:tile-detail', kwargs={'tile_id':tile_obj.pk}),
        'form': tile_form,
        'form_type': 'edit',

    }
    return render(request, 'tiles/tiles-tile-detail.html', context=context)

def tile_create_view(request, section_id):
    section_obj = PageSection.objects.get(pk=section_id)
    print('section_obj', section_obj)
    tile_form = TileForm(request.POST or None, section_obj=section_obj)
    context = {
        'section_obj': section_obj,
        'post_url': reverse('tiles:tile-create', kwargs={'section_id':section_id}),
        'form': tile_form,
        'form_type': 'create',
    }
    

    if tile_form.is_valid():
        tile_obj = tile_form.save()
        tile_form = TileForm(request.POST or None, section_obj=section_obj)
        context = {
            'section_obj': section_obj,
            'post_url': reverse('tiles:tile-detail', kwargs={'tile_id':tile_obj.pk}),
            'form': tile_form,
            'tile_obj': tile_obj,
            'form_type': 'edit',
        }
        
    return render(request, 'tiles/tiles-tile-detail.html', context=context)
    



#### Tiles UI

def tiles_main_view(request):
    return render(request, 'tiles/tiles-main.html')

def tiles_scene_view(request):
    return render(request, 'tiles/scene-tile.html')

def tiles_nav_view(request):
    return render(request, 'tiles/nav-tile.html')

def tiles_page_view(request):
    
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

    return render(request, 'tiles/tiles-pages.html', context=context)



def pages_view(request):
    return render(request, 'tiles/tiles-pages.html')


#reverse('scenes:device-list', kwargs={'scene_id':scene_obj.pk}),