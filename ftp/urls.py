from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^reload$', views.reload),
    url(r'^delete$', views.delete),
    url(r'^create$', views.create),
    url(r'^password$', views.password),
    url(r'^status$', views.status),
]
