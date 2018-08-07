from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os, json, datetime
from ftp.models import *

# Create your views here.
@login_required
def index(request):
    filter = request.GET.get('filter', '')
    if filter:
        dataset = User.objects.filter(Q(name__contains=filter)|Q(path__contains=filter)|Q(comment__contains=filter)).order_by("id")
    else:
        dataset = User.objects.all().order_by("id")
    paginator = Paginator(dataset, 25) ## Show 25 content per page
    page = request.GET.get('page')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    user = {
        'name': request.user,
        'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return render(request, "ftp.html", { "content": content, 'filter' : filter, 'user' : user })

@login_required
def reload(request):
    try:
        post = json.loads(request.body)
        sync_status = post['sync_status']
        if int(sync_status) == 1:
            if os.path.isfile(settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd'):
                with open(settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd') as f:
                    for line in f:
                        ftpuser_name = line.split(':')[0]
                        ftpuser_password = line.split(':')[1]
                        ftpuser_path = line.split(':')[5].rstrip('/./')
                        if line.split(':')[-3]:
                            ftpuser_status = 0
                        else:
                            ftpuser_status = 1
                        if User.objects.filter(name=ftpuser_name).exists():
                            ftpuser_update = User.objects.get(name = ftpuser_name)
                            ftpuser_update.password =  ftpuser_password
                            ftpuser_update.path = ftpuser_path
                            ftpuser_update.status = ftpuser_status
                            ftpuser_update.save()
                        else:
                            ftpuser_create = User(name = ftpuser_name, password = ftpuser_password, path = ftpuser_path, status = ftpuser_status)
                            ftpuser_create.save()
                os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.pdb' + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
                content = { 'flag': 'Success' }
            else:
                content = { 'flag': 'Error', 'content': 'ftp账号不存在' }
        else:
            content = { 'flag': 'Error', 'content': '参数错误' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def create(request):
    try:
        post = json.loads(request.body)
        ftpuser_create = User(name = post['name'], password = post['password'], path = post['path'], status = 1, comment = post['comment'])
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw useradd ' + post['name'] + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd' + ' -u ' + settings.OPTIONS['run_user'] + ' -g ' + settings.OPTIONS['run_user'] + ' -d ' + post['path'] + ' -m <<EOF \n' + post['password'] + '\n' + post['password'] + '\nEOF')
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.pdb' + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
        ftpuser_create.save()
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def delete(request):
    try:
        post = json.loads(request.body)
        username = User.objects.get(id=post['id']).name
        User.objects.filter(id=post['id']).delete()
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw userdel ' + username + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.pdb' + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def password(request):
    try:
        post = json.loads(request.body)
        username = User.objects.get(id=post['id']).name
        new_password=post['password']
        User.objects.filter(id=post['id']).update(password=new_password)
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw passwd ' + username + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd' + ' <<EOF \n' + new_password + '\n' + new_password + '\nEOF')
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.pdb' + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def status(request):
    try:
        post = json.loads(request.body)
        status = post['status']
        username = User.objects.get(id=post['id']).name
        if int(status) == 0:
            os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw usermod ' + username + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd' + ' -r 1')
        else:
            os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw usermod ' + username + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd' + ' -r ""')
        User.objects.filter(id=post['id']).update(status=status)
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.pdb' + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)
