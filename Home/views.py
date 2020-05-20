from django.shortcuts import render
from django.http import HttpResponse

from django.conf import settings

BASE_DIR = settings.BASE_DIR # .../[Dir]/Deductions
PARENT_DIR = settings.PARENT_DIR # .../[Dir]/
RAW_DIR = settings.RAW_DIR # .../[Dir]/Raw

from Post.models import Post

# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-date_uploaded')
    return render(request, 'home/index.html', {'posts': posts})