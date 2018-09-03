from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
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
    data = User.objects.get(is_superuser=1)
    content = model_to_dict(data)
    #print({ "content": content, 'user' : user })
    return render(request, 'setting.html', { "content": content, 'user' : user })

@login_required
def update_password(request):
    try:
        post = json.loads(request.body)
        newpassword = post['password']
        user = User.objects.get(pk=post['id'])
        user.set_password(newpassword)
        user.save()
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { "flag":"Error","context":str(e) }
    return JsonResponse(content)

@login_required
def update_username(request):
    try:
        post = json.loads(request.body)
        newusername = post['username']
        user = User.objects.get(pk=post['id'])
        user.username=newusername
        user.save()
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'context': str(e) }
    return JsonResponse(content)

@login_required
def update_profile(request):
    try:
        post = json.loads(request.body)
        newemail = post['email']
        user = User.objects.get(pk=post['id'])
        user.email=newemail
        user.save()
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'context': str(e) }
    return JsonResponse(content)
