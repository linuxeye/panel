from django.db import models
from website.models import Website

# Create your models here.
'''用户表'''
class User(models.Model): 
    addtime = models.DateTimeField(auto_now=True, auto_created=True)
    dbuser = models.CharField(max_length=50)
    dbhost = models.CharField(max_length=50)
    dbpassword = models.CharField(max_length=128, blank=True, null=True, default='')
    comment = models.CharField(max_length=255, blank=True, null=True, default='')
    class Meta:
        unique_together = ('dbuser', 'dbhost',) #user,host联合唯一

'''数据库信息表'''
class Database(models.Model):
    addtime = models.DateTimeField(auto_now=True, auto_created=True)
    dbname = models.CharField(max_length=50,unique=True) #库唯一
    dbaddr = models.CharField(max_length=30,default='localhost')
    comment = models.CharField(max_length=255, blank=True, null=True, default='')

'''权限对应表'''
class Permission(models.Model):
    YES = 'Y'
    NO = 'N'
    YES_OR_NO_CHOICES = ((YES,'Yes'),(NO,'No')) #定义字段选择
    addtime = models.DateTimeField(auto_now=True, auto_created=True)
    dbname = models.CharField(max_length=50)
    dbuser = models.CharField(max_length=50)
    dbhost = models.CharField(max_length=50)
    select_priv = models.CharField(max_length=2,choices=YES_OR_NO_CHOICES,default=NO)
    insert_priv = models.CharField(max_length=2,choices=YES_OR_NO_CHOICES,default=NO)
    update_priv = models.CharField(max_length=2,choices=YES_OR_NO_CHOICES,default=NO)
    delete_priv = models.CharField(max_length=2,choices=YES_OR_NO_CHOICES,default=NO)
    comment = models.CharField(max_length=255, blank=True, null=True, default='')
