from django.db import models

# Create your models here.
class Post(models.Model):
    id = models.CharField(max_length= 20, primary_key=True)
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=50)
    author_profile_link = models.CharField(max_length=1000)
    description = models.CharField(max_length=2000)
    manifest_url = models.CharField(max_length = 1000)
    tags = models.CharField(max_length=1000)
    date_uploaded = models.DateTimeField()
    date_last_modified = models.DateTimeField()
    total_hits = models.CharField(max_length=100, default='0')
    dir_name = models.CharField(max_length=1000)