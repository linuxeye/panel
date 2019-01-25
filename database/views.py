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

    """
    功能：显示相关数据到前端
    """
    
    users = User.objects.all()
    databases = Database.objects.all()
    content = {
        'users': users
        'databases' : databases
    }
    return render(request, "database.html", content)

@login_required
def CreateUser(request):

    """
    功能：创建数据库用户
    """

    '''使用json.loads方法获取post数据'''
    post = json.loads(request.body)
    user = post['user']
    host = post['host']
    password = post['password']
    comment = post['comment']
    
    '''定义执行语句'''
    create_user_sql = "CREATE USER %s@%s IDENTIFIED BY '%s';" % (user,host,password) #创建用户语句
    
    '''做判断逻辑，判断用户输入数据不存在sqlite中'''
    if not User.objects.filter(dbuser = post['user'],dbhost = post['host']).exists():
        try:
            '''将用户输入的数据存入sqlite，调用MysqlManager方法执行创建用户动作，反馈给用户成功信息'''
            dbuser_create = User(dbuser = post['user'], dbhost = post['host'], dbpassword = post['password'], comment = post['comment'])
            dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))
            dbManager.execute(create_user_sql)
            result = user + '用户创建成功！'
            content = { 'flag': 'Success', 'content': result}
            dbuser_create.save()
        except Exception as e:
            content = { 'flag': 'Error', 'content': str(e) }
    else:
        content = {'flag': 'Error', 'content': '输入的用户名和主机联合存在！'}
    return JsonResponse(content)

@login_required
def CreateDatabase(request):

    """
    功能：创建数据库
    """

    '''使用json.loads方法获取post数据'''
    post = json.loads(request.body)
    dbname = post['dbname']
    dbaddr = post['dbaddr']
    comment = post['comment']

    '''定义执行语句'''
    create_database_sql = "CREATE DATABASE IF NOT EXISTS %s CHARACTER SET utf8mb4;" % (dbname) #创建库语句

    '''做判断逻辑，判断用户输入数据不存在sqlite中'''
    if not Database.objects.filter(dbname = post['dbname']).exists():
        try:
            '''将用户输入的数据存入sqlite，调用MysqlManager方法执行创建数据库动作，反馈给用户成功信息'''
            database_create = Database(dbname = post['dbname'], dbaddr = post['dbaddr'], comment = post['comment'])
            dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))
            dbManager.execute(create_database_sql)
            result = dbname + '创建成功！'
            content = { 'flag': 'Success', 'content': result}
            database_create.save()
        except Exception as e:
            content = { 'flag': 'Error', 'content': str(e) }
    else:
            content = {'flag': 'Error', 'content': '输入的库已经存在！'}
    return JsonResponse(content)

@login_required
def GrantUser(request):

    """
    功能：给已经存在的用户进行赋权
    """

    '''使用json.loads方法获取post数据'''
    post = json.loads(request.body)
    dbname = post['dbname']
    dbuser = post['user']
    dbhost = post['host']
    dbauth = post['auth']
    comment = post['comment']

    '''定义执行语句'''
    grant_user_sql = "GRANT ALL PRIVILEGES ON %s.* TO %s@'%s'" % (dbname,dbuser,dbhost) #赋权语句

    '''做判断逻辑，判断数据库存在'''
    if  Database.objects.filter(dbname = post['dbname']).exists():
        if not Permission.objects.filter(dbuser = post['user'],dbhost = post['host']).exists():
            try:
                dbgrant_create = Permission(dbname = post['dbname'], dbuser = post['user'], dbhost = post['host'], select_priv = post['auth'], insert_priv = post['auth'], update_priv = post['auth'], delete_priv = post['auth'], comment = post['comment'])
                dbManager = MysqlManager("mysql", 'root', eval(OPTIONS['dbrootpwd']))
                dbManager.execute(grant_user_sql)
                result = dbuser + '赋权成功！'
                content = { 'flag': 'Success', 'content': result}
                dbgrant_create.save()
            except Exception as e:
                content = { 'flag': 'Error', 'content': str(e) }
        else:
            content = {'flag': 'Error', 'content': '权限表中存在该用户，要对表进行更新操作而不是增加数据操作'}
    else:
        content = {'flag': 'Error', 'content': '输入的库不存在！不能进行赋权'}
    return JsonResponse(content)

