from django.urls import include, re_path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^login/$', LoginView.as_view(template_name='login.html')),
    re_path(r'^logout/$', LogoutView.as_view(next_page='/')),
    re_path(r'^superuser/$', views.create_superuser),
    re_path(r'^setting/', include('setting.urls')),
    re_path(r'^ftp/', include('ftp.urls')),
    re_path(r'^crontab/', include('crontab.urls')),
]
