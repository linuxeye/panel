from django.db import models

# Create your models here.
class Crontab(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True, default='')
    time = models.CharField(max_length=150, blank=True, null=True, default='')
    script = models.CharField(max_length=300, blank=True, null=True, default='')
    status = models.BooleanField(default=1)
    addtime = models.DateTimeField(auto_now=True, auto_created=True)
