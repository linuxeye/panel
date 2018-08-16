from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
@login_required
def index(request):
    user = {
        'name': request.user,
        'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return render(request, "website.html", {'user': user})
