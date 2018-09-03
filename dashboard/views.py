from django.shortcuts import render
import os, json, platform, psutil, time, datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import RequestContext

# Create your views here.
@login_required
def index(request):
    user = {
        'name': request.user,
        'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return render(request, "dashboard.html", {'user': user})

@login_required
def uptime(request):
    """
    Get uptime
    """
    try:
        uptime = {}
        all_sec = time.time() - psutil.boot_time()
        MINUTE,HOUR,DAY = 60,3600,86400
        uptime['day'] = int(all_sec / DAY )
        uptime['hour'] = int((all_sec % DAY) / HOUR)
        uptime['minute'] = int((all_sec % HOUR) / MINUTE)
        #uptime['second'] = int(all_sec % MINUTE)
        #uptime_time = str(timedelta(seconds=uptime_seconds))
        #data = uptime_time.split('.', 1)[0]
    except Exception as err:
        uptime = str(err)
    #return uptime
    return JsonResponse(uptime)
    #return render(request, "dashboard.html", {'uptime': uptime})

def get_ipaddress():
    """
    Get the IP Address
    """
    data = []
    try:
        eth = os.popen("ip addr | grep LOWER_UP | awk '{print $2}'")
        iface = eth.read().strip().replace(':', '').split('\n')
        eth.close()
        del iface[0]
        for i in iface:
            pipe = os.popen("ip addr show " + i + "| awk '{if ($2 == \"forever\"){!$2} else {print $2}}'")
            data1 = pipe.read().strip().split('\n')
            pipe.close()
            if len(data1) == 2:
                data1.append('unavailable')
            if len(data1) == 3:
                data1.append('unavailable')
            data1[0] = i
            data.append(data1)
        ips = {'interface': iface, 'itfip': data}
        data = ips
    except Exception as err:
        data = str(err)
    return data

def get_cpus():
    """
    Get the number of CPUs and model/type
    """
    try:
        pipe = os.popen("cat /proc/cpuinfo |" + "grep 'model name'")
        data = pipe.read().split(':')[-1].strip()
        pipe.close()
        if not data:
            pipe = os.popen("cat /proc/cpuinfo |" + "grep 'Processor'")
            data = pipe.read().split(':')[-1].strip()
            pipe.close()
        cpus = psutil.cpu_count()
        data = {'cpus': cpus, 'type': data}
    except Exception as err:
        data = str(err)
    return data

def get_users():
    """
    Get the current logged in users
    """
    try:
        suser_list = []
        suser_dict = {}
        for u in psutil.users():
            suser_dict['name'] = u.name
            suser_dict['terminal'] = u.terminal
            suser_dict['host'] = u.host
            #suser_list.append(suser_dict)
            suser_list.append(" ".join(suser_dict.values()))
        if suser_list == [""]:
            suser_list = None
        else:
            suser_list = [i.split(None, 3) for i in suser_list]
    except Exception as err:
        suser_list = str(err)
    return suser_list

def get_traffic(request):
    """
    Get the traffic for the specified interface
    """
    try:
        pipe = os.popen("cat /proc/net/dev |" + "grep " + request + "| awk '{print $1, $9}'")
        data = pipe.read().strip().split(':', 1)[-1]
        pipe.close()
        if not data[0].isdigit():
            pipe = os.popen("cat /proc/net/dev |" + "grep " + request + "| awk '{print $2, $10}'")
            data = pipe.read().strip().split(':', 1)[-1]
            pipe.close()
        data = data.split()
        traffic_in = int(data[0])
        traffic_out = int(data[1])
        all_traffic = {'traffic_in': traffic_in, 'traffic_out': traffic_out}
        data = all_traffic
    except Exception as err:
        data = str(err)
    return data

def get_platform():
    """
    Get the OS name, hostname and kernel
    """
    try:
        osname = " ".join(platform.linux_distribution())
        uname = platform.uname()
        if osname == '  ':
            osname = uname[0]
        data = {'osname': osname, 'hostname': uname[1], 'kernel': uname[2]}
    except Exception as err:
        data = str(err)
    return data

def get_disk():
    """
    Get disk usage
    """
    try:
        pipe = os.popen("df -Ph | " + "grep -v Filesystem | " + "awk '{print $1, $2, $3, $4, $5, $6}'")
        data = pipe.read().strip().split('\n')
        pipe.close()
        data = [i.split(None, 6) for i in data]
    except Exception as err:
        data = str(err)
    return data

def get_disk_rw():
    """
    Get the disk reads and writes
    """
    try:
        pipe = os.popen("cat /proc/partitions | grep -v 'major' | awk '{print $4}'")
        data = pipe.read().strip().split('\n')
        pipe.close()
        rws = []
        for i in data:
            if i.isalpha():
                pipe = os.popen("cat /proc/diskstats | grep -w '" + i + "'|awk '{print $4, $8}'")
                rw = pipe.read().strip().split()
                pipe.close()
                rws.append([i, rw[0], rw[1]])
        if not rws:
            pipe = os.popen("cat /proc/diskstats | grep -w '" + data[0] + "'|awk '{print $4, $8}'")
            rw = pipe.read().strip().split()
            pipe.close()
            rws.append([data[0], rw[0], rw[1]])
        data = rws
    except Exception as err:
        data = str(err)
    return data

def get_mem():
    """
    Get memory usage
    """
    try:
        pipe = os.popen(
            "free -tm | " + "grep 'Mem' | " + "awk '{print $2,$4,$6,$7}'")
        data = pipe.read().strip().split()
        pipe.close()
        allmem = int(data[0])
        freemem = int(data[1])
        buffers = int(data[2])
        cachedmem = int(data[3])
        # Memory in buffers + cached is actually available, so we count it
        # as free. See http://www.linuxatemyram.com/ for details
        freemem += buffers + cachedmem
        percent = (100 - ((freemem * 100) / allmem))
        usage = (allmem - freemem)
        mem_usage = {'usage': usage, 'buffers': buffers, 'cached': cachedmem, 'free': freemem, 'percent': percent}
        data = mem_usage
    except Exception as err:
        data = str(err)
    return data

def get_cpu_usage():
    """
    Get the CPU usage and running processes
    """
    try:
        pipe = os.popen("ps aux --sort -%cpu,-rss")
        data = pipe.read().strip().split('\n')
        pipe.close()
        usage = [i.split(None, 10) for i in data]
        del usage[0]
        total_usage = []
        for element in usage:
            usage_cpu = element[2]
            total_usage.append(usage_cpu)
        total_usage = sum(float(i) for i in total_usage)
        total_free = ((100 * int(get_cpus()['cpus'])) - float(total_usage))
        cpu_used = {'free': total_free, 'used': float(total_usage), 'all': usage}
        data = cpu_used
    except Exception as err:
        data = str(err)
    return data

def get_load():
    """
    Get load average
    """
    try:
        data = os.getloadavg()[0]
    except Exception as err:
        data = str(err)
    return data

def get_netstat():
    """
    Get ports and applications
    """
    try:
        pipe = os.popen(
            "ss -tnp | grep ESTAB | awk '{print $4, $5}'| sed 's/::ffff://g' | awk -F: '{print $1, $2}' "
            "| awk 'NF > 0' | sort -n | uniq -c")
        data = pipe.read().strip().split('\n')
        pipe.close()
        data = [i.split(None, 4) for i in data]
    except Exception as err:
        data = str(err)
    return data

@login_required
def getnetstat(request):
    """
    Return netstat output
    """
    try:
        net_stat = get_netstat()
    except Exception:
        net_stat = None
    data = json.dumps(net_stat)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required
def general(request, name):
    """
    Return the hostname
    """
    getplatform = get_platform()
    hostname = getplatform['hostname']
    osname = getplatform['osname']
    kernel = getplatform['kernel']
    data = {}
    if name == 'hostname':
        try:
            data = hostname
        except Exception:
            data = None
    if name == 'osname':
        try:
            data = osname
        except Exception:
            data = None
    if name == 'kernel':
        try:
            data = kernel
        except Exception:
            data = None
    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required
def getcpus(request, name):
    """
    Return the CPU number and type/model
    """
    cpus = get_cpus()
    print(cpus)
    cputype = cpus['type']
    cpucount = cpus['cpus']
    data = {}
    if name == 'type':
        try:
            data = cputype
        except Exception:
            data = None
    if name == 'count':
        try:
            data = cpucount
        except Exception:
            data = None
    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required
def getdisk(request):
    """
    Return the disk usage
    """
    try:
        diskusage = get_disk()
    except Exception:
        diskusage = None
    data = json.dumps(diskusage)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required
def getips(request):
    """
    Return the IPs and interfaces
    """
    try:
        get_ips = get_ipaddress()
    except Exception:
        get_ips = None
    data = json.dumps(get_ips['itfip'])
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required
def getusers(request):
    """
    Return online users
    """
    try:
        online_users = get_users()
    except Exception:
        online_users = None

    data = json.dumps(online_users)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required
def getproc(request):
    """
    Return the running processes
    """
    try:
        processes = get_cpu_usage()
        processes = processes['all']
    except Exception:
        processes = None
    data = json.dumps(processes)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required
def cpuusage(request):
    """
    Return CPU Usage in %
    """
    try:
        cpu_usage = get_cpu_usage()
    except Exception:
        cpu_usage = 0
    cpu = [
        {
            "value": cpu_usage['free'],
            "color": "#0AD11B"
        },
        {
            "value": cpu_usage['used'],
            "color": "#F7464A"
        }
    ]

    data = json.dumps(cpu)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required
def memusage(request):
    """
    Return Memory Usage in % and numeric
    """
    datasets_free = []
    datasets_used = []
    datasets_buffers = []
    datasets_cached = []
    try:
        mem_usage = get_mem()
    except Exception:
        mem_usage = 0
    try:
        cookies = request.COOKIES['memory_usage']
    except Exception:
        cookies = None
    if not cookies:
        datasets_free.append(0)
        datasets_used.append(0)
        datasets_buffers.append(0)
        datasets_cached.append(0)
    else:
        datasets = json.loads(cookies)
        datasets_free = datasets[0]
        datasets_used = datasets[1]
        datasets_buffers = datasets[2]
        datasets_cached = datasets[3]

    if len(datasets_free) > 10:
        while datasets_free:
            del datasets_free[0]
            if len(datasets_free) == 10:
                break
    if len(datasets_used) > 10:
        while datasets_used:
            del datasets_used[0]
            if len(datasets_used) == 10:
                break
    if len(datasets_buffers) > 10:
        while datasets_buffers:
            del datasets_buffers[0]
            if len(datasets_buffers) == 10:
                break
    if len(datasets_cached) > 10:
        while datasets_cached:
            del datasets_cached[0]
            if len(datasets_cached) == 10:
                break
    if len(datasets_free) <= 9:
        datasets_free.append(int(mem_usage['free']))
    if len(datasets_free) == 10:
        datasets_free.append(int(mem_usage['free']))
        del datasets_free[0]
    if len(datasets_used) <= 9:
        datasets_used.append(int(mem_usage['usage']))
    if len(datasets_used) == 10:
        datasets_used.append(int(mem_usage['usage']))
        del datasets_used[0]
    if len(datasets_buffers) <= 9:
        datasets_buffers.append(int(mem_usage['buffers']))
    if len(datasets_buffers) == 10:
        datasets_buffers.append(int(mem_usage['buffers']))
        del datasets_buffers[0]
    if len(datasets_cached) <= 9:
        datasets_cached.append(int(mem_usage['cached']))
    if len(datasets_cached) == 10:
        datasets_cached.append(int(mem_usage['cached']))
        del datasets_cached[0]

    # Some fix division by 0 Chart.js
    if len(datasets_free) == 10:
        if sum(datasets_free) == 0:
            datasets_free[9] += 0.1
        if sum(datasets_free) / 10 == datasets_free[0]:
            datasets_free[9] += 0.1

    memory = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(247,70,74,0.5)",
                "strokeColor": "rgba(247,70,74,1)",
                "pointColor": "rgba(247,70,74,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_used
            },
            {
                "fillColor": "rgba(43,214,66,0.5)",
                "strokeColor": "rgba(43,214,66,1)",
                "pointColor": "rgba(43,214,66,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_free
            },
            {
                "fillColor": "rgba(0,154,205,0.5)",
                "strokeColor": "rgba(0,154,205,1)",
                "pointColor": "rgba(0,154,205,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_buffers
            },
            {
                "fillColor": "rgba(255,185,15,0.5)",
                "strokeColor": "rgba(255,185,15,1)",
                "pointColor": "rgba(265,185,15,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_cached
            }
        ]
    }

    cookie_memory = [datasets_free, datasets_used, datasets_buffers, datasets_cached]
    data = json.dumps(memory)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['memory_usage'] = cookie_memory
    response.write(data)
    return response

@login_required
def loadaverage(request):
    """
    Return Load Average numeric
    """
    datasets = []
    try:
        load_average = get_load()
    except Exception:
        load_average = 0

    try:
        cookies = request.COOKIES['load_average']
    except Exception:
        cookies = None

    if not cookies:
        datasets.append(0)
    else:
        datasets = json.loads(cookies)
    if len(datasets) > 10:
        while datasets:
            del datasets[0]
            if len(datasets) == 10:
                break
    if len(datasets) <= 9:
        datasets.append(float(load_average))
    if len(datasets) == 10:
        datasets.append(float(load_average))
        del datasets[0]

    # Some fix division by 0 Chart.js
    if len(datasets) == 10:
        if sum(datasets) == 0:
            datasets[9] += 0.1
        if sum(datasets) / 10 == datasets[0]:
            datasets[9] += 0.1

    load = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(151,187,205,0.5)",
                "strokeColor": "rgba(151,187,205,1)",
                "pointColor": "rgba(151,187,205,1)",
                "pointStrokeColor": "#fff",
                "data": datasets
            }
        ]
    }

    data = json.dumps(load)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['load_average'] = datasets
    response.write(data)
    return response

@login_required
def gettraffic(request):
    """
    Return the traffic for the interface
    """
    datasets_in = []
    datasets_in_i = []
    datasets_out = []
    datasets_out_o = []
    label = "KBps"

    try:
        intf = get_ipaddress()
        intf = intf['interface'][0]
        traffic = get_traffic(intf)
    except Exception:
        traffic = 0
    try:
        cookies = request.COOKIES['traffic']
    except Exception:
        cookies = None
    if not cookies:
        datasets_in.append(0)
        datasets_in_i.append(0)
        datasets_out.append(0)
        datasets_out_o.append(0)
    else:
        datasets = json.loads(cookies)
        datasets_in = datasets[0]
        datasets_out = datasets[1]
        datasets_in_i = datasets[2]
        datasets_out_o = datasets[3]

    if len(datasets_in) > 10:
        while datasets_in:
            del datasets_in[0]
            if len(datasets_in) == 10:
                break
    if len(datasets_in_i) > 2:
        while datasets_in_i:
            del datasets_in_i[0]
            if len(datasets_in_i) == 2:
                break
    if len(datasets_out) > 10:
        while datasets_out:
            del datasets_out[0]
            if len(datasets_out) == 10:
                break
    if len(datasets_out_o) > 2:
        while datasets_out_o:
            del datasets_out_o[0]
            if len(datasets_out_o) == 2:
                break

    if len(datasets_in_i) <= 1:
        datasets_in_i.append(float(traffic['traffic_in']))
    if len(datasets_in_i) == 2:
        datasets_in_i.append(float(traffic['traffic_in']))
        del datasets_in_i[0]
    if len(datasets_out_o) <= 1:
        datasets_out_o.append(float(traffic['traffic_out']))
    if len(datasets_out_o) == 2:
        datasets_out_o.append(float(traffic['traffic_out']))
        del datasets_out_o[0]

    dataset_in = (float(((datasets_in_i[1] - datasets_in_i[0]) / 1024) / (time_refresh_net / 1000)))
    dataset_out = (float(((datasets_out_o[1] - datasets_out_o[0]) / 1024) / (time_refresh_net / 1000)))

    if dataset_in > 1024 or dataset_out > 1024:
        dataset_in = (float(dataset_in / 1024))
        dataset_out = (float(dataset_out / 1024))
        label = "MBps"

    if len(datasets_in) <= 9:
        datasets_in.append(dataset_in)
    if len(datasets_in) == 10:
        datasets_in.append(dataset_in)
        del datasets_in[0]
    if len(datasets_out) <= 9:
        datasets_out.append(dataset_out)
    if len(datasets_out) == 10:
        datasets_out.append(dataset_out)
        del datasets_out[0]

    # Some fix division by 0 Chart.js
    if len(datasets_in) == 10:
        if sum(datasets_in) == 0:
            datasets_in[9] += 0.1
        if sum(datasets_in) / 10 == datasets_in[0]:
            datasets_in[9] += 0.1

    traff = {
        'labels': [label] * 10,
        'datasets': [
            {
                "fillColor": "rgba(105,210,231,0.5)",
                "strokeColor": "rgba(105,210,231,1)",
                "pointColor": "rgba(105,210,231,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_in
            },
            {
                "fillColor": "rgba(227,48,81,0.5)",
                "strokeColor": "rgba(227,48,81,1)",
                "pointColor": "rgba(227,48,81,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_out
            }
        ]
    }

    cookie_traffic = [datasets_in, datasets_out, datasets_in_i, datasets_out_o]
    data = json.dumps(traff)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['traffic'] = cookie_traffic
    response.write(data)
    return response

@login_required
def getdiskio(request):
    """
    Return the reads and writes for the drive
    """
    datasets_in = []
    datasets_in_i = []
    datasets_out = []
    datasets_out_o = []
    try:
        diskrw = get_disk_rw()
        diskrw = diskrw[0]
    except Exception:
        diskrw = 0

    try:
        cookies = request.COOKIES['diskrw']
    except Exception:
        cookies = None

    if not cookies:
        datasets_in.append(0)
        datasets_in_i.append(0)
        datasets_out.append(0)
        datasets_out_o.append(0)
    else:
        datasets = json.loads(cookies)
        datasets_in = datasets[0]
        datasets_out = datasets[1]
        datasets_in_i = datasets[2]
        datasets_out_o = datasets[3]

    if len(datasets_in) > 10:
        while datasets_in:
            del datasets_in[0]
            if len(datasets_in) == 10:
                break
    if len(datasets_in_i) > 2:
        while datasets_in_i:
            del datasets_in_i[0]
            if len(datasets_in_i) == 2:
                break
    if len(datasets_out) > 10:
        while datasets_out:
            del datasets_out[0]
            if len(datasets_out) == 10:
                break
    if len(datasets_out_o) > 2:
        while datasets_out_o:
            del datasets_out_o[0]
            if len(datasets_out_o) == 2:
                break

    if len(datasets_in_i) <= 1:
        datasets_in_i.append(int(diskrw[1]))
    if len(datasets_in_i) == 2:
        datasets_in_i.append(int(diskrw[1]))
        del datasets_in_i[0]
    if len(datasets_out_o) <= 1:
        datasets_out_o.append(int(diskrw[2]))
    if len(datasets_out_o) == 2:
        datasets_out_o.append(int(diskrw[2]))
        del datasets_out_o[0]

    dataset_in = (int((datasets_in_i[1] - datasets_in_i[0]) / (time_refresh_net / 1000)))
    dataset_out = (int((datasets_out_o[1] - datasets_out_o[0]) / (time_refresh_net / 1000)))

    if len(datasets_in) <= 9:
        datasets_in.append(dataset_in)
    if len(datasets_in) == 10:
        datasets_in.append(dataset_in)
        del datasets_in[0]
    if len(datasets_out) <= 9:
        datasets_out.append(dataset_out)
    if len(datasets_out) == 10:
        datasets_out.append(dataset_out)
        del datasets_out[0]

    # Some fix division by 0 Chart.js
    if len(datasets_in) == 10:
        if sum(datasets_in) == 0:
            datasets_in[9] += 0.1
        if sum(datasets_in) / 10 == datasets_in[0]:
            datasets_in[9] += 0.1
    disk_rw = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(245,134,15,0.5)",
                "strokeColor": "rgba(245,134,15,1)",
                "pointColor": "rgba(245,134,15,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_in
            },
            {
                "fillColor": "rgba(15,103,245,0.5)",
                "strokeColor": "rgba(15,103,245,1)",
                "pointColor": "rgba(15,103,245,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_out
            }
        ]
    }
    cookie_diskrw = [datasets_in, datasets_out, datasets_in_i, datasets_out_o]
    data = json.dumps(disk_rw)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['diskrw'] = cookie_diskrw
    response.write(data)
    return response
def chunks(get, n):
    return [get[i:i + n] for i in range(0, len(get), n)]
