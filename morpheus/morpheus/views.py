import os, json
from django.views import View
from django.shortcuts import render, HttpResponse
from utilities.logging import SystemLogger
from hue.hub import Hub
current_file_directory = os.path.dirname(os.path.abspath(__file__))

class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)
    
def navbar_view(request):
    return render(request, 'navbar.html')
    