from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict

from deducted.models import Deducted

import json

PARENT_FOLDER = 'deducted/'

# Create your views here.
def home(request):
    deductions = Deducted.objects.all()
    fresh = deductions.order_by('-date_uploaded')[0]
    latest_modified = deductions.order_by('-date_last_modified')[0]
    context = {
        'fresh': fresh,
        'latest_modified': latest_modified,
        'deductions': deductions,
    }
    return render(request, 'home/index.html', context)

def folder_format(path):
    if path[-1]!='/':
        path+= '/'
    return path
