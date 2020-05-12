from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.template import loader

from datetime import datetime
import os
from bs4 import BeautifulSoup
import requests
import pytz
from urllib.parse import unquote

from deducted.models import Deducted

IST = pytz.timezone('Asia/Kolkata')

PARENT_DIR = ''
PRE_DIR = 'deducted/'

# PARENT_DIR = '/home/deductions/Deductions/'
# PRE_DIR = ''

# Create your views here.
def site_admin(request):
    return render(request, 'site-admin/index.html')

def fetch_deduction_info(request, manifest_url):

    try:
        deducted = Deducted.objects.get(manifest_url=manifest_url)
    except:
        deducted = None

    curr_time = timezone.now().astimezone(IST)

    deduction_id =  deducted.id if deducted else curr_time.strftime('%Y%m%d%H%M%S')

    manifest = requests.get(manifest_url)
    manifest = manifest.json()

    title = manifest['title']
    description = manifest['description']
    author = manifest['author']
    author_profile_link =  manifest['author_profile_link']

    try:
        page_type = manifest['page_type']
    except:
        page_type = 'Independent'

    static = ', '.join(manifest['static']) if manifest['static'] else 'None'
    templates = ', '.join(manifest['templates']) if manifest['templates'] else 'None'

    scripts = ', '.join(manifest['data']['script']) if manifest['data']['script'] else 'None'
    extra = ', '.join(manifest['data']['data']) if manifest['data']['data'] else 'None'

    date_uploaded = deducted.date_uploaded.strftime('%d %b, %Y %I:%M:%S %p') if deducted else curr_time.strftime('%d %b, %Y %I:%M:%S %p')
    date_last_modified = curr_time.strftime('%d %b, %Y %I:%M:%S %p')

    fetched_info = {
        'manifest_url': manifest_url,
        'page_type': page_type,
        'id': deduction_id,
        'title': title,
        'description': description,
        'author': author+' ['+author_profile_link+']',
        'static': static,
        'templates': templates,
        'scripts': scripts,
        'extra': extra,
        'date_uploaded': date_uploaded,
        'date_last_modified': date_last_modified,
        'exists': bool(deducted),
    }

    request.session['id'] = fetched_info['id']
    request.session['page_type'] = fetched_info['page_type']
    request.session['author'] = author
    request.session['author_profile_link'] = author_profile_link
    request.session['manifest_url'] = fetched_info['manifest_url']
    request.session['date_uploaded'] = fetched_info['date_uploaded']
    request.session['date_last_modified'] = fetched_info['date_last_modified']

    html = loader.render_to_string('add-deduction/fetched-info.html', fetched_info)
    return JsonResponse({'html': html})

def add_page_to_database(request):

    logs = []

    manifest_url = request.session['manifest_url']
    slashes = [i for i, c in enumerate(manifest_url) if c == "/"]
    folder_name = folder_format( manifest_url[ (slashes[-2]+1):slashes[-1] ] )

    logs.append(['s', 'Directory decided: '+folder_name])

    logs += download_file(manifest_url, 'manifest.json', PARENT_DIR + PRE_DIR +'static/'+folder_name)
    manifest = requests.get(manifest_url).json()

    static = manifest['static']
    templates = manifest['templates']
    scripts = manifest['data']['script']
    
    for fl in static:
        logs += download_file(
            manifest_url[:-13]+'static/'+fl,
            fl,
            PARENT_DIR + PRE_DIR +'static/'+folder_name
        )

    for fl in templates:
        logs += download_file(
            manifest_url[:-13]+'templates/'+fl,
            fl,
            PARENT_DIR +'deducted/templates/'+folder_name
        )

    for fl in scripts:
        logs += download_file(
            manifest_url[:-13]+'static/'+fl,
            fl,
            PARENT_DIR + PRE_DIR  +'static/'+folder_name
        )

    try:
        Deducted(
            id = request.session['id'],
            title = request.GET.get('title'),
            author = request.session['author'],
            author_profile_link = request.session['author_profile_link'],
            description = request.GET.get('description'),
            manifest_url = request.session['manifest_url'],
            tags = request.GET.get('tags'),
            date_uploaded = datetime.strptime(request.session['date_uploaded'], '%d %b, %Y %I:%M:%S %p').astimezone(IST),
            date_last_modified = datetime.strptime(request.session['date_last_modified'], '%d %b, %Y %I:%M:%S %p').astimezone(IST),
            dir_name=folder_name,
        ).save()
        logs.append(['s', 'Deduction Saved.'])
    except Exception as e:
        logs.append(['e', str(e)])
        
    logs.reverse()
    html = loader.render_to_string('add-deduction/logs.html', {'logs': logs})

    return JsonResponse({'html': html})

def add_deduction(request):

    request_type = request.GET.get('request-type')
    if request_type == 'fetch-info':
        manifest_url = request.GET.get('manifest-url')
        manifest_url = unquote(manifest_url)
        return fetch_deduction_info(request, manifest_url)
    elif request_type == 'add-deduction':
        return add_page_to_database(request)

    return render(request, 'add-deduction/index.html')

def refresh_fetch_deduction_info(deductions):

    all_manifest = []
    for deduction in deductions:
        print('Fetching... ', deduction)

        manifest = deduction.manifest_url

        manifest = requests.get(manifest)
        manifest = manifest.json()

        static = ', '.join(manifest['static']) if manifest['static'] else 'None'
        templates = ', '.join(manifest['templates']) if manifest['templates'] else 'None'

        scripts = ', '.join(manifest['data']['script']) if manifest['data']['script'] else 'None'
        extra = ', '.join(manifest['data']['data']) if manifest['data']['data'] else 'None'
        
        all_manifest.append(
            {
                'id': deduction.id, 'title': deduction.title, 'manifest_url': deduction.manifest_url,
                'static': static, 'templates': templates, 'scripts': scripts, 'extra': extra,
            }
        )
    return all_manifest

def refresh_download_files(manifest_url):

    logs = []

    slashes = [i for i, c in enumerate(manifest_url) if c == "/"]
    folder_name = folder_format( manifest_url[ (slashes[-2]+1):slashes[-1] ] )

    logs.append(['s', 'Directory decided: '+folder_name])

    logs += download_file(manifest_url, 'manifest.json', PARENT_DIR + PRE_DIR +'static/'+folder_name)
    manifest = requests.get(manifest_url).json()

    static = manifest['static']
    templates = manifest['templates']
    scripts = manifest['data']['script']
    
    for fl in static:
        logs += download_file(
            manifest_url[:-13]+'static/'+fl,
            fl,
            PARENT_DIR + PRE_DIR +'static/'+folder_name
        )

    for fl in templates:
        logs += download_file(
            manifest_url[:-13]+'templates/'+fl,
            fl,
            PARENT_DIR +'deducted/templates/'+folder_name
        )

    for fl in scripts:
        logs += download_file(
            manifest_url[:-13]+'static/'+fl,
            fl,
            PARENT_DIR + PRE_DIR  +'static/'+folder_name
        )

    print(logs)

    return logs

def refresh_files(request):
    deductions = Deducted.objects.all()
    all_manifest = refresh_fetch_deduction_info(deductions)
    print(all_manifest)
    for manifest in all_manifest:
        refresh_download_files(manifest['manifest_url'])
    return JsonResponse({})

def download_file(url, name, path='temp/'):
    logs = []
    path = folder_format(path)
    if url:
        try:
            os.makedirs(path)
            logs.append(['s', 'Directory created: '+path])
        except Exception as e:
            logs.append(['e', str(e)])

        try:
            r = requests.get(url, allow_redirects=True)
            f = open(path+name, 'wb')
            f.write(r.content)
            f.close()
            logs.append(['s', 'File downloaded: '+path+name])
        except Exception as e:
            logs.append(['e', str(e)])
    else:
        logs.append(['e', 'Invalid URL: '+url])
    return logs

def folder_format(path):
    if path[-1]!='/':
        path+= '/'
    return path
