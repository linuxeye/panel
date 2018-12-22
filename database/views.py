from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json,datetime
from panel.settings import OPTIONS
from database.mysql_manager import MysqlManager
from libs import public
from database.models import *

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
    """
    获取post数据
    判断用户输入的数据库名是否唯一、用户名和主机是否联合唯一（数据比较在SQLite中）
    若两个中有一个不唯一都反馈给用户已存在的消息
    若两个都不存在，将用户输入信息存入sqlite中，并执行SQL语句，反馈给用户执行成功信息
    """
    '''使用json.loads方法获取post数据'''
    if request.method == "POST":
        post = json.loads(request.body)
        dbname = post['name']
        dbuser = post['user']
        dbpassword = post['password']
        dbhost = post['host']
        dbcoment = post['comment']
        '''做判断逻辑，判断数据不存在'''
        if not Database.objects.filter(dbname = post['name']).exists():
            if not Database.objects.filter(dbuser = post['user'],dbhost = post['host']).exists():
                try:
                    '''将用户输入的数据存入sqlite，调用MysqlManager方法执行创建数据库、用户，并进行赋权动作，反馈给用户成功信息'''
                    dbuser_create = Database(dbname = post['name'], dbuser = post['user'], dbpassword = post['password'], dbhost = post['host'], comment = post['comment'])
                    dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))
                    create_database_sql = "CREATE DATABASE IF NOT EXISTS %s CHARACTER SET utf8;" % (dbname)
                    create_user_sql = "CREATE USER %s@%s IDENTIFIED BY '%s';" % (dbuser,dbhost,dbpassword)
                    grant_user_sql = "GRANT ALL PRIVILEGES ON %s.* TO %s@'%s'" % (dbname,dbuser,dbhost)
                    dbManager.execute(create_database_sql)
                    dbManager.execute(create_user_sql)
                    dbManager.execute(grant_user_sql)
                    

                    result = dbname + '创建和赋权成功！'
                    content = { 'flag': 'Success', 'content': result}
                    dbuser_create.save()
                except Exception as e:
                    content = { 'flag': 'Error', 'content': str(e) }
            else:
                content = {'flag': 'Error', 'content': '输入的用户名和主机联合存在！'}
        else:
            content = {'flag': 'Error', 'content': '输入的库已经存在！'}
        return JsonResponse(content)
    else:
        return HttpResponse(u'有误！')

def Delatabase(request):
    dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))

