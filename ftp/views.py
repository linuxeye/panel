# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os,json
from django.core import serializers
#from ftp.forms import *
from ftp.models import *

@login_required
def reload(request):
    os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb')
    return HttpResponse(settings.OPTIONS)

def index(request):
    dataset = User.objects.filter().all()
    data0 = serializers.serialize("json", dataset) 
    content = list()
    for i in json.JSONDecoder().decode(data0):
        j = i['fields']
        j['id'] = i['pk']
        content.append(j)
    #print(content)
    return render(request, "ftp.html", { "content": content})

#def adduser(request):

def deleteuser(request):
    try:
        post = json.loads(request.body)
        User.objects.filter(id=post['id']).delete()
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'context': str(e) }
    return JsonResponse(content)

@login_required
def setpassword(request):
    try:
        post = json.loads(request.body)
        username = User.objects.get(id=post['id']) 
        new_password=post['password']
        User.objects.filter(id=post['id']).update(password=post['password'])
        print(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw passwd ' + username + '<<EOF \n' + new_password + '\n' + new_password + '\nEOF')
        #os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw passwd ' + username + '<<EOF \n' + new_password + '\n' + new_password + '\nEOF')
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'context': str(e) }
    return JsonResponse(content)

@login_required
def setstatus(request):
    try:
        post = json.loads(request.body)
        User.objects.filter(id=post['id']).update(status=post['status'])
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'context': str(e) }
    return JsonResponse(content)
