from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^password/$', views.modify_pass),
    url(r'^admin/$', views.admin_reset),
]
