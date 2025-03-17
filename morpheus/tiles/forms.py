from django import forms
from .models import Page, PageSection
from .choices import PageTypes, TileTypes

page_types = PageTypes()
tile_types = TileTypes()

class PageForm(forms.ModelForm):
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    ),
    page_type = forms.ChoiceField(
        choices=page_types.get_page_types_choices(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    

    class Meta:
        model = Page
        fields = ['name','id','page_type']

    def clean(self):
        data = self.cleaned_data
        return data
    

class SectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.page_obj = kwargs.pop('page_obj', None)
        super().__init__(*args, **kwargs)

        if self.page_obj:
            self.fields['page'].initial = self.page_obj

    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    ),
    page = forms.TextInput(
        # widget=forms.ChoiceWidget(
        #     attrs={
        #         'class': 'form-control',
        #     }
        # )
    )
    sort = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
    class Meta:
        model = PageSection
        fields = ['name','page','sort']

    def clean(self):
        data = self.cleaned_data
        return data
    


class TileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.section_obj = kwargs.pop('section_obj', None)
        super().__init__(*args, **kwargs)
    
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    ),
  
    tile_type = forms.ChoiceField(
        choices=tile_types.get_tile_types_choices(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    tile_object_id = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    sort = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
    class Meta:
        model = PageSection
        fields = ['name','page','sort']

    def clean(self):
        data = self.cleaned_data
        return data

