from django.shortcuts import render 
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
import json

def index(request):
    if not bool(User.objects.all().count()):
        return HttpResponseRedirect('/superuser')
    else:
        return HttpResponseRedirect(settings.LOGIN_URL)

def create_superuser(request):
    if bool(User.objects.all().count()):
        #context = { "flag": "Error", "context": "superuser Already exist" }
        #return JsonResponse(context)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        if request.method == 'POST':
            try:
                #post = request.POST
                post = json.loads(request.body) 
                User.objects.create_superuser(username=post['username'], email=None, password=post['password'])
                context = {'flag': 'Success'}
            except Exception as e:
                context = {'flag': 'Error', 'context': str(e)}
            print(context)
            print(locals())
            return JsonResponse(context)
        return render(request, 'superuser.html', locals())
