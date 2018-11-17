from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from libs import public
import os, json, time

# Create your views here.
@login_required
def index(request):
    setting = json.loads(public.readfile('data/setting.json'))
    user = {
        'name': request.user,
        'date': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    }
    #return JsonResponse(context)
    data = User.objects.get(is_superuser=1)
    content = model_to_dict(data)
    content['port'] = int(public.readfile('data/port.conf').strip())
    return render(request, 'setting.html', { "content": content, "setting": setting, 'user' : user })

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
        import signal
        post = json.loads(request.body)
        newport= post['port']
        newemail = post['email']
        newetitle = post['title']
        subkey = ['title']
        oldport = int(public.readfile('data/port.conf').strip())
        pid = int(public.readfile('logs/runconfig.py.pid').strip())
        old_setting_dict = json.loads(public.readfile('data/setting.json'))
        if newetitle != old_setting_dict[subkey[0]]:
            setting_json = dict([(key, post[key]) for key in subkey])
            public.writefile('data/setting.json', json.dumps(setting_json))
            print(pid)
            os.kill(pid,signal.SIGHUP)
        if oldport != newport:
            public.writefile('data/port.conf', newport)
            os.kill(pid,signal.SIGHUP)
        user = User.objects.get(pk=post['id'])
        user.email=newemail
        user.save()
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'context': str(e) }
    return JsonResponse(content)
