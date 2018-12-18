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
        post = json.loads(request.body)
        dbname = post['name']
        #dbname = request.POST.get('name','')
        dbuser = request.POST.get('user','')
        dbpassword = request.POST.get('password','')
        dbhost = request.POST.get('host','')
        dbcoment = request.POST.get('comment','')
        try:
            dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))
            createsql = 'CREATE DATABASE' + ' ' + 'IF NOT EXISTS' + ' ' + dbname + ' ' + 'CHARACTER SET utf8'
            #createsql = 'CREATE DATABASE test CHARACTER SET utf8'
            result = dbManager.create(createsql)
            content = { 'flag': 'Success', 'comm': str(createsql), 'res': str(result) }
            #if result:
            #    content = { 'flag': 'Success', 'comm': str(createsql), 'res': str(result) }
            #else:
            #    content = {'flag': 'create failed'}
        except Exception as e:
            content = { 'flag': 'Error', 'content': str(e) }
        return JsonResponse(content)
        #output = {'data': dbname}
        #return render(request,'test.html',output)
    else:
        return HttpResponse(u'有误！')

def Delatabase(request):
    dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))

#name=post['name'], user=post['user'], password=post['password'], host=post['host'], comment=post['comment']
