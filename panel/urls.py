"""panel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf.urls import url, include
#from django.contrib import admin
#from django.urls import path
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'next_page': "/"}),
    url(r'^superuser/$', views.create_superuser),
    url(r'^setting/', include('setting.urls')),
    url(r'^ftp/', include('ftp.urls')),
    url(r'^crontab/', include('crontab.urls')),
]
