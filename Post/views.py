from django.shortcuts import render

import os, json
from bs4 import BeautifulSoup

from django.conf import settings
from Post.models import Post

BASE_DIR = settings.BASE_DIR # .../[Dir]/Deductions
PARENT_DIR = settings.PARENT_DIR # .../[Dir]/
RAW_DIR = settings.RAW_DIR # .../[Dir]/Raw

# Create your views here.
def post(request, post_id):
    post_id = post_id[-14:]
    post = Post.objects.get(id=post_id)
    manifest = os.path.join(RAW_DIR, post.dir_name, 'manifest.json')
    with open(manifest, 'r') as mf:
        manifest = json.load(mf)
    try:
        page_type = manifest['page_type']
    except:
        pass
    if page_type=='Typora':
        with open(os.path.join(RAW_DIR, post.dir_name, 'templates', 'index.html'), 'r') as html:
            html = BeautifulSoup(html.read(), 'lxml')
        html = str(html.body)
        html = html.replace('body', 'div')
        return render(request, 'post/index.html', {'html': html, 'post': post})
    else:
        context = {}
        scripts = manifest['data']['script']
        if scripts:
            f_script = os.path.join(RAW_DIR, post.dir_name, 'static', scripts[0])
            f_content = os.path.join(RAW_DIR, post.dir_name, 'static', 'content.xml')
            import importlib
            spec = importlib.util.spec_from_file_location('script', f_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            context = module.get_context(f_content)
        context['post'] = post
        return render(request, os.path.join(post.dir_name, 'templates', 'index.html'), context)
