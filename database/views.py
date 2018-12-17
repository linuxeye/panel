from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json,datetime
from panel.settings import OPTIONS
from database.mysql_manager import MysqlManager
from libs import public
from django.contrib.auth.models import User
# Create your views here.
@login_required
def index(request):
    setting = json.loads(public.readfile('data/setting.json'))
    user = {
        'name': request.user,
        'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return render(request, "database.html", {"setting": setting, 'user': user})

@login_required
def AddDatabase(request):
    dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))
    result = dbManager.query("show databases;")
    print(result)
    if result:
         content = { 'flag': 'Success' }
    else:
         content = { 'Error': 'test'}
    return JsonResponse(content)
def CreateDatabase(request):
    if request.method == "POST":
        dbname = request.POST.get('name','')
        dbuser = request.POST.get('user','')
        dbpassword = request.POST.get('password','')
        dbhost = request.POST.get('host','')
        dbcoment = request.POST.get('comment','')
        try:
            post = json.loads(request.body)
            #dbuser_create = User(name = post['name'], user=post['user'], password = post['password'], host=post['host'], comment=post['comment'])
            #dbuser_create.save()
            content = { 'flag': 'Success' }
        except Exception as e:
            content = { 'flag': 'Error', 'content': str(e) }
        return JsonResponse(content)
    else:
        return HttpResponse(u'有误！')

def Delatabase(request):
    dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))

#name=post['name'], user=post['user'], password=post['password'], host=post['host'], comment=post['comment']