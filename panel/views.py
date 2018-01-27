from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
import json

def index(request):
    if not bool(User.objects.all().count()):
        return HttpResponseRedirect('/superuser/') 
    else:
        return HttpResponseRedirect('/login/')

def create_superuser(request):
    if bool(User.objects.all().count()):
        #context = { "flag": "Error", "context": "superuser Already exist" }
        #return JsonResponse(context)
        return HttpResponseRedirect('/home')
    else:
        if request.method == "POST":
            try:
                #post = request.POST
                post = json.loads(request.body) 
                User.objects.create_superuser(username=post['username'], email=None, password=post['password'])
                context = {'flag': "Success",}
            except Exception as e:
                context = { "flag":"Error", "context":str(e) }
            return JsonResponse(context)
        return render_to_response('superuser.html')
