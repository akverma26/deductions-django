from django.shortcuts import render

from .models import Deducted

from bs4 import BeautifulSoup
import json

PARENT_DIR = ''
PRE_DIR = 'deducted/'

# PARENT_DIR = '/home/deductions/Deductions/'
# PRE_DIR = ''

# Create your views here.
def deducted(request, deduction_id):
    deduction = Deducted.objects.get(id=deduction_id[-14:])
    dir_name = folder_format(deduction.dir_name)
    manifest = PARENT_DIR + PRE_DIR +'static/'+dir_name+'manifest.json'
    with open(manifest, 'r') as mf:
        manifest = json.load(mf)
    
    try:
        page_type = manifest['page_type']
    except:
        pass

    if page_type=='Typora':
        with open(PARENT_DIR +'deducted/templates/'+dir_name+'index.html', 'r') as html:
            html = BeautifulSoup(html.read(), 'lxml')
        html = str(html.body)
        html = html.replace('body', 'div')
        return render(request, 'deducted/index.html', {'html':html, 'deduction':deduction})
    else:

        context = {}
        script = manifest['data']['script']
        if script:
            f_script = PARENT_DIR + PRE_DIR + 'static/' + dir_name + script[0]
            f_content = PARENT_DIR + PRE_DIR + 'static/' + dir_name + 'content.xml'
            import importlib
            spec = importlib.util.spec_from_file_location('script', f_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            context = module.get_context(f_content)

        context['deduction'] = deduction
        return render(request, dir_name+'index.html', context)

def new(request):
    pass

def folder_format(path):
    if path[-1]!='/':
        path+= '/'
    return path