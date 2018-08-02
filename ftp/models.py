from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=True, null=True, default='')
    password = models.CharField(max_length=128, blank=True, null=True, default='')
    path = models.FilePathField(max_length=255, blank=True, null=True, default='')
    status = models.BooleanField(default=1)
    addtime = models.DateTimeField(auto_now=True, auto_created=True)
    comment = models.CharField(max_length=255, blank=True, null=True, default='')
