from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse, JsonResponse
import json,time

# Create your views here.
@login_required
def index(request):
    user = {
        'name': request.user,
        'date': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    }

    #return JsonResponse(context)
    return render(request, 'setting.html', { 'user' : user })

@login_required
def modify_password(request):
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
                content = { 'flag': 'Success' }
            else:
                content = { 'flag': 'Error', 'context': 'VerifyFaild' }
    except Exception as e:
        content = { "flag":"Error","context":str(e) }
    return JsonResponse(content)

@login_required
def modify_username(request):
    try:
        post = request.POST
        username_password = post['password']
        new_username=post['new_username']
        user = User.objects.get(username=request.user)
        if user.check_password(username_password):
            user.username=new_username
            user.save()
            content = { 'flag': 'Success' }
        else:
            content = { 'flag': 'Error', 'context': 'VerifyFaild' }
    except Exception as e:
        content = { 'flag': 'Error', 'context': str(e) }
    return JsonResponse(content)
