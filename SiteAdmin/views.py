from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json, pytz
from datetime import datetime

from Post.models import Post

IST = pytz.timezone('Asia/Kolkata')

# Create your views here.
def make_databse(request):
    with open('SiteAdmin/database.json', 'r') as db:
        database = json.load(db)
    for d in database:
        Post(
            id = database[d]['id'],
            title = database[d]['title'],
            author = database[d]['author'],
            author_profile_link = database[d]['author_profile_link'],
            description = database[d]['description'],
            manifest_url = database[d]['manifest_url'],
            tags = database[d]['tags'],
            date_uploaded = datetime.strptime(database[d]['date_uploaded'], '%d %b, %Y %I:%M:%S %p').astimezone(IST),
            date_last_modified = datetime.strptime(database[d]['date_last_modified'], '%d %b, %Y %I:%M:%S %p').astimezone(IST),
            dir_name = database[d]['dir_name'],
        ).save()
    return JsonResponse({'Status': 'Done'})