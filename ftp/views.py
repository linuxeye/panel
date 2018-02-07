# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os, json, datetime
#from django.core import serializers
from ftp.models import *
#from ftp.forms import *

@login_required
def index(request):
    filter = request.GET.get('filter', '')
    if filter:
        dataset = User.objects.filter(Q(name__contains=filter)|Q(path__contains=filter)|Q(comment__contains=filter)).order_by("id")
    else:
        dataset = User.objects.all().order_by("id")
    paginator = Paginator(dataset, 25) ## Show 25 content per page
    page = request.GET.get('page')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    user = {
        'name': request.user,
        'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    }
    return render(request, "ftp.html", { "content": content, 'filter' : filter, 'user' : user })

@login_required
def reload(request):
    with open(settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd') as f:
        for line in f:
            ftpuser_name = line.split(':')[0]
            ftpuser_password = line.split(':')[1]
            ftpuser_path = line.split(':')[5].rstrip('/./')
            if line.split(':')[-3]:
                ftpuser_status = 0
            else:
                ftpuser_status = 1
            #print(ftpuser_name,ftpuser_path,ftpuser_status,line.split(':')[-3])
            if User.objects.filter(name=ftpuser_name).exists():
                ftpuser_update = User.objects.get(name = ftpuser_name)
                ftpuser_update.password =  ftpuser_password
                ftpuser_update.path = ftpuser_path
                ftpuser_update.status = ftpuser_status
                ftpuser_update.save()
            else:
                ftpuser_create = User(name = ftpuser_name, password = ftpuser_password, path = ftpuser_path, status = ftpuser_status)
                ftpuser_create.save()
            content = { 'flag': 'Success' }
    os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.pdb' + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
    return HttpResponse(content)

#def adduser(request):

@login_required
def deleteuser(request):
    try:
        post = json.loads(request.body)
        User.objects.filter(id=post['id']).delete()
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def setpassword(request):
    try:
        post = json.loads(request.body)
        username = User.objects.get(id=post['id']) 
        new_password=post['password']
        User.objects.filter(id=post['id']).update(password=post['password'])
        print(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw passwd ' + username + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd' + '<<EOF \n' + new_password + '\n' + new_password + '\nEOF')
        print(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.pdb' + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def setstatus(request):
    try:
        post = json.loads(request.body)
        status = post['status']
        username = User.objects.get(id=post['id']).name 
        #print(username,status)
        if int(status) == 0:
            os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw usermod ' + username + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd' + ' -r 1')
        else:
            os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw usermod ' + username + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd' + ' -r ""')
        User.objects.filter(id=post['id']).update(status=status)
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.pdb' + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)
