from django.db import models
from website.models import Website

# Create your models here.
class Database(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    dbname = models.CharField(max_length=50, unique=True)
    dbuser = models.CharField(max_length=50, unique=True)
    dbhost = models.CharField(max_length=50)
    dbpassword = models.CharField(max_length=128, blank=True, null=True, default='')
    addtime = models.DateTimeField(auto_now=True, auto_created=True)
    comment = models.CharField(max_length=255, blank=True, null=True, default='')
