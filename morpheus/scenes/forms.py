from django import forms
from .models import Scene

class SceneForm(forms.ModelForm):
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Scene
        fields = '__all__'

    def clean(self):
        data = self.cleaned_data
        return data