from django.db import models
from website.models import Website

# Create your models here.
class Database(models.Model):
    YES = 'Y'
    NO = 'N'
    YES_OR_NO_CHOICES = ((YES,'Yes'),(NO,'No'))
    website = models.ForeignKey(Website, null=True, on_delete=models.CASCADE)
    dbname = models.CharField(max_length=50)
    dbaddr = models.CharField(max_length=50)
    dbuser = models.CharField(max_length=50)
    dbhost = models.CharField(max_length=50)
    dbpassword = models.CharField(max_length=128, blank=True, null=True, default='')
    select_priv = models.CharField(max_length=2,choices=YES_OR_NO_CHOICES,default=NO)
    insert_priv = models.CharField(max_length=2,choices=YES_OR_NO_CHOICES,default=NO)
    update_priv = models.CharField(max_length=2,choices=YES_OR_NO_CHOICES,default=NO)
    delete_priv = models.CharField(max_length=2,choices=YES_OR_NO_CHOICES,default=NO)
    addtime = models.DateTimeField(auto_now=True, auto_created=True)
    dbcomment = models.CharField(max_length=255, blank=True, null=True, default='')
    usercomment = models.CharField(max_length=255, blank=True, null=True, default='')
    class Meta:
        unique_together = ('dbuser', 'dbhost',)