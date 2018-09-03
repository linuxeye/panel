from django.shortcuts import render
from django.contrib.auth.models import User
from panel.settings import LOGIN_URL, LOGIN_REDIRECT_URL 
from django.http import JsonResponse, HttpResponseRedirect
import json

def index(request):
    if not bool(User.objects.all().count()):
        return HttpResponseRedirect('/register')
    else:
        return HttpResponseRedirect(LOGIN_URL)

def register(request):
    if bool(User.objects.all().count()):
        return HttpResponseRedirect(LOGIN_REDIRECT_URL)
    else:
        if request.method == 'POST':
            try:
                post = json.loads(request.body)
                User.objects.create_superuser(username=post['username'], email=post['email'], password=post['password'])
                context = {'flag': 'Success'}
            except Exception as e:
                context = {'flag': 'Error', 'context': str(e)}
            #print(context)
            #print(locals())
            return JsonResponse(context)
        return render(request, 'register.html', locals())
