from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^$', views.index, name='main'),
    re_path(r'^info/uptime/$', views.uptime, name='uptime'),
    re_path(r'^info/memory/$', views.memusage, name='memusage'),
    re_path(r'^info/cpuusage/$', views.cpuusage, name='cpuusage'),
    re_path(r'^info/getdisk/$', views.getdisk, name='getdisk'),
    re_path(r'^info/getusers/$', views.getusers, name='getusers'),
    re_path(r'^info/getips/$', views.getips, name='getips'),
    re_path(r'^info/gettraffic/$', views.gettraffic, name='gettraffic'),
    re_path(r'^info/proc/$', views.getproc, name='getproc'),
    re_path(r'^info/getdiskio/$', views.getdiskio, name='getdiskio'),
    re_path(r'^info/loadaverage/$', views.loadaverage, name='loadaverage'),
    re_path(r'^info/platform/([\w\-\.]+)/$', views.general, name='platform'),
    re_path(r'^info/getcpus/([\w\-\.]+)/$', views.getcpus, name='getcpus'),
    re_path(r'^info/getnetstat/$', views.getnetstat, name='getnetstat'),
]
