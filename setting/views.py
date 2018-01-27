# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse, JsonResponse
import json,time

@login_required(login_url="/login/")
def index(request):
    user = {
        'name': request.user,
        'date': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    }

    nic = {
        'nics': 'test',
        'internal_nic': 'setting coming soon'
    }

    #return JsonResponse(context)
    return render_to_response('setting.html',{ 'user' : user , 'nic' : nic })

@login_required(login_url="/login/")
def modify_pass(request):
    try:
        post = request.POST
        old_pass = post['old_password']
        new_pass = post['new_password']
        verify_pass = post['verify_password']
        if old_pass and new_pass and verify_pass:
            user = User.objects.get(username=request.user)
            if user.check_password(old_pass) and new_pass == verify_pass:
                user.set_password(verify_pass)
                user.save()
                content = { "flag":"Success" }
            else:
                content = { "flag":"Error","context":"VerifyFaild" }
    except Exception as e:
        content = { "flag":"Error","context":str(e) }

    return JsonResponse(content)

@login_required(login_url="/login/")
def admin_reset(request):
    try:
        post = request.POST
        admin_pass = post['password']
        new_admin=post['new_superuser']
        user = User.objects.get(username=request.user)
        print(admin_pass,new_admin,user)
        if user.check_password(admin_pass):
            user.username=new_admin
            user.save()
            content = { "flag":"Success" }
        else:
            content = { "flag":"Error","context":"VerifyFaild" }
    except Exception as e:
        content = { "flag":"Error","context":str(e) }

    return JsonResponse(content)
    #return HttpResponse(json.dumps(content))
