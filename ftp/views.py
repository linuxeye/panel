# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os
#from ftp.forms import *
#from ftp.models import *

@login_required
def reload(request):
    os.system(settings.OPTIONS['pureftpd_install_dir'] + '/bin/pure-pw mkdb')
    return HttpResponse(settings.OPTIONS)

#def adduser(request):

#def deleteuser(request):

#def resetpassword(request):

#def setstatus(request):
