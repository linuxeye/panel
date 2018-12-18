from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json,datetime
from panel.settings import OPTIONS
from database.mysql_manager import MysqlManager
from libs import public
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
    #print(result)
    if result:
         content = { 'flag': 'Success', 'com': result }
    else:
         content = { 'Error': 'test'}
    return JsonResponse(content)
def CreateDatabase(request):
    if request.method == "POST":
        post = json.loads(request.body)
        dbname = post['name']
        dbuser = post['user']
        dbpassword = post['password']
        dbhost = post['host']
        dbcoment = post['comment']
        dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))
        data = dbManager.query("show databases;")
        if dbname not in data:
            try:
                dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))
                createsql = 'CREATE DATABASE' + ' ' + 'IF NOT EXISTS' + ' ' + dbname + ' ' + 'CHARACTER SET utf8'
                dbManager.create(createsql)
                result = dbname + '数据库创建成功！'
                content = { 'flag': 'Success', 'comm': result}
            except Exception as e:
                content = { 'flag': 'Error', 'content': str(e) }
        else:
            content = {'flag': 'Error', 'content': '该库已经存在！'}
        return JsonResponse(content)
    else:
        return HttpResponse(u'有误！')

def Delatabase(request):
    dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))

