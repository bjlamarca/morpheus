from django import forms
from .models import Page
from .choices import PageTypes

page_types = PageTypes()

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
        fields = ['name','id']

    def clean(self):
        data = self.cleaned_data
        return data
    

