from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^reload$', views.reload),
    url(r'^delete$', views.deleteuser),
    url(r'^setpassword$', views.setpassword),
    url(r'^setstatus$', views.setstatus),
]
