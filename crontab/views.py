from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os, json, datetime, platform
from libs import public
from crontab.models import *

# Create your views here.
@login_required
def index(request):
    setting = json.loads(public.readfile('data/setting.json'))
    filter = request.GET.get('filter', '')
    if filter:
        dataset = Crontab.objects.filter(Q(name__contains=filter)|Q(time__contains=filter)|Q(script__contains=filter)).order_by("id")
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
    return render(request, "crontab.html", { "content": content, 'filter' : filter, "setting": setting, 'user' : user })

@login_required
def reload(request):
    try:
        post = json.loads(request.body)
        sync_status = post['sync_status']
        if platform.dist()[0] in ['centos', 'redhat', 'fedora']:
            cron_file = '/var/spool/cron/root'
        else:
            cron_file = '/var/spool/cron/crontabs/root'
        if int(sync_status) == 1:
            with open(cron_file) as f:
                for line in f:
                    if len(line.strip()):
                        if '#' not in line:
                            crontab_status = 1
                        else:
                            line=line.lstrip('#').lstrip()
                            crontab_status = 0
                        crontab_time = ' '.join(line.strip().split()[0:5])
                        crontab_job = ' '.join(line.split()[5:])
                        if '#' in crontab_job:
                            crontab_script = ' '.join(crontab_job.rsplit('#')[:-1])
                        else:
                            crontab_script = crontab_job
                        if "ntpdate" in crontab_script:
                            crontab_name = 'Sync time'
                        elif "acme.sh" in crontab_script:
                            crontab_name = 'LetsEncrypt Renew'
                        else:
                            crontab_name = ' '.join(crontab_job.rsplit('#')[1:])
                        if Crontab.objects.filter(time = crontab_time).filter(script = crontab_script).exists():
                            crontab_update = Crontab.objects.filter(time = crontab_time).filter(script = crontab_script).update(name = crontab_name, status = crontab_status)
                        else:
                            crontab_create = Crontab(name = crontab_name, time = crontab_time, script=crontab_script, status = crontab_status)
                            crontab_create.save()
            content = { 'flag': 'Success' }
        else:
            content = { 'flag': 'Error', 'content': u'参数错误' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def create(request):
    try:
        post = json.loads(request.body)
        crontab_name = post['name'].strip()
        crontab_time = post['time'].strip()
        crontab_script = post['script'].strip()
        crontab_job = crontab_time + ' ' + crontab_script + '\n'
        if platform.dist()[0] in ['centos', 'redhat', 'fedora']:
            cron_file = '/var/spool/cron/root'
        else:
            cron_file = '/var/spool/cron/crontabs/root'
        if Crontab.objects.filter(time = crontab_time).filter(script = crontab_script).exists():
            content = { 'flag': 'Error', 'content': 'The task already exist' }
        else:
            crontab_data = []
            crontab_data.append(crontab_job)
            with open(cron_file, 'a+') as f:
                f.writelines(crontab_data)
            crontab_create = Crontab(name = crontab_name, time = crontab_time, script = crontab_script)
            crontab_create.save()
            content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def delete(request):
    try:
        post = json.loads(request.body)
        if platform.dist()[0] in ['centos', 'redhat', 'fedora']:
            cron_file = '/var/spool/cron/root'
        else:
            cron_file = '/var/spool/cron/crontabs/root'
        crontab_script = Crontab.objects.get(id=post['id']).script
        crontab_data = []
        with open(cron_file, 'r+') as f:
            for line in f.readlines():
                if line.strip():
                    crontab_data.append(line)
        for i,item in enumerate(crontab_data):
            if crontab_script in item:
                crontab_data.pop(i)
        with open(cron_file, 'r+') as f:
            f.seek(0)
            f.truncate()
            f.writelines(crontab_data)
        Crontab.objects.filter(id=post['id']).delete()
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def status(request):
    try:
        post = json.loads(request.body)
        status = post['status']
        if platform.dist()[0] in ['centos', 'redhat', 'fedora']:
            cron_file = '/var/spool/cron/root'
        else:
            cron_file = '/var/spool/cron/crontabs/root'
        crontab_name = Crontab.objects.get(id=post['id']).name
        crontab_script = Crontab.objects.get(id=post['id']).script

        crontab_data = []
        if int(status) == 0:
            with open(cron_file, 'r+') as f:
                for line in f.readlines():
                    if line.strip():
                        if crontab_script in line:
                            line = '#' + line
                        crontab_data.append(line)
            with open(cron_file, 'r+') as f:
                f.seek(0)
                f.truncate()
                f.writelines(crontab_data)
        else:
            with open(cron_file, 'r+') as f:
                for line in f.readlines():
                    if line.strip():
                        if crontab_script in line:
                            line=line.lstrip('#')
                        crontab_data.append(line)
            with open(cron_file, 'r+') as f:
                f.seek(0)
                f.truncate()
                f.writelines(crontab_data)
        Crontab.objects.filter(id=post['id']).update(status=status)
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)

@login_required
def update(request):
    try:
        post = json.loads(request.body)
        crontab_name = Crontab.objects.get(id=post['id']).name
        crontab_time = Crontab.objects.get(id=post['id']).time
        crontab_script = Crontab.objects.get(id=post['id']).script
        crontab_newname = post['name'].strip()
        crontab_newtime = post['time'].strip()
        crontab_newscript = post['script'].strip()
        Crontab.objects.filter(id=post['id']).update(name = crontab_newname, time = crontab_newtime, script = crontab_newscript)
        Crontab_List = Crontab.objects.all().values_list('time','script','status')
        if crontab_newname != crontab_name or crontab_newtime != crontab_time:
            if platform.dist()[0] in ['centos', 'redhat', 'fedora']:
                cron_file = '/var/spool/cron/root'
            else:
                cron_file = '/var/spool/cron/crontabs/root'
            crontab_data = []
            for crontab in Crontab_List:
                if crontab[2]:
                    crontab_job = crontab[0] + ' ' + crontab[1] + '\n'
                else:
                    crontab_job = '#' + crontab[0] + ' ' + crontab[1] + '\n'
                crontab_data.append(crontab_job)
            #print(crontab_data)
            with open(cron_file, 'r+') as f:
                f.seek(0)
                f.truncate()
                f.writelines(crontab_data)
        content = { 'flag': 'Success' }
    except Exception as e:
        content = { 'flag': 'Error', 'content': str(e) }
    return JsonResponse(content)
