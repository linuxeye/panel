from django.db import models

# Create your models here.
class Website(models.Model):
    stack = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=50, unique=True)
    path = models.FilePathField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=1)
    addtime = models.DateTimeField(auto_now=True, auto_created=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

class Domain(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    port = models.IntegerField(default=80)
    addtime = models.DateTimeField(auto_now=True, auto_created=True)
