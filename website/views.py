from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from libs import public
import json,datetime

# Create your views here.
@login_required
def index(request):
    setting = json.loads(public.readfile('data/setting.json'))
    user = {
        'name': request.user,
        'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return render(request, "website.html", {"setting": setting, 'user': user})
