from django.db import models

# Create your models here.
class Website(models.Model):
    domain = models.CharField(max_length=50, unique=True)
    stack = models.IntegerField(default=1)
    path = models.FilePathField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=50)
    ssl = models.BooleanField(default=0) 
    addtime = models.DateTimeField(auto_now=True, auto_created=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
