from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os, json, datetime, platform
from crontab.models import *

# Create your views here.
@login_required
def index(request):
    filter = request.GET.get('filter', '')
    if filter:
        dataset = Crontab.objects.filter(Q(name__contains=filter)|Q(time__contains=filter)|Q(context__contains=filter)|Q(comment__contains=filter)).order_by("id")
    else:
        dataset = Crontab.objects.all().order_by("id")
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
    return render(request, "crontab.html", { "content": content, 'filter' : filter, 'user' : user })

@login_required
def reload(request):
    try:
        post = json.loads(request.body)
        sync_status = post['sync_status']
        if platform.dist()[0] in ['centos', 'redhat']:
            cron_file = '/var/spool/cron/root'
        else:
            cron_file = '/var/spool/cron/crontabs/root'
        if int(sync_status) == 1:
            with open(cron_file) as f:
                for line in f:
                    if '#' not in line:
                        crontab_status = 1
                    else:
                        line=line.lstrip('#').lstrip()
                        crontab_status = 0
                    crontab_time = ' '.join(line.strip().split()[0:5])
                    crontab_script = ' '.join(line.split()[5:])
                    if Crontab.objects.filter(time = crontab_time).filter(script = crontab_script).exists():
                        crontab_update = Crontab.objects.filter(time = crontab_time).filter(script = crontab_script).update(status = crontab_status)
                    else:
                        crontab_create = Crontab(time = crontab_time, script=crontab_script, status = crontab_status)
                        crontab_create.save()
            content = { 'flag': 'Success' }
        else:
            content = { 'flag': 'Error', 'content': '参数错误' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def create(request):
    try:
        post = json.loads(request.body)
        crontab_create = Crontab(name = post['name'], password = post['password'], path = post['path'], status = 1, comment = post['comment'])
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw useradd ' + post['name'] + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd' + ' -u ' + settings.OPTIONS['run_user'] + ' -g ' + settings.OPTIONS['run_user'] + ' -d ' + post['path'] + ' -m <<EOF \n' + post['password'] + '\n' + post['password'] + '\nEOF')
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.pdb' + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
        crontab_create.save()
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def delete(request):
    try:
        post = json.loads(request.body)
        username = Crontab.objects.get(id=post['id']).name 
        Crontab.objects.filter(id=post['id']).delete()
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
        username = Crontab.objects.get(id=post['id']).name 
        new_password=post['password']
        Crontab.objects.filter(id=post['id']).update(password=new_password)
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
        if platform.dist()[0] in ['centos', 'redhat']:
            cron_file = '/var/spool/cron/root'
        else:
            cron_file = '/var/spool/cron/crontabs/root'
        crontab_time = Crontab.objects.get(id=post['id']).time
        crontab_script = Crontab.objects.get(id=post['id']).script
        if int(status) == 0:
            os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw usermod ' + username + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd' + ' -r 1')
        else:
            os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw usermod ' + username + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd' + ' -r ""')
        Crontab.objects.filter(id=post['id']).update(status=status)
        os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.pdb' + ' -f ' + settings.OPTIONS['pureftpd_install_dir'] + '/etc/pureftpd.passwd')
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)
