from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^reload$', views.reload),
    re_path(r'^delete$', views.delete),
    re_path(r'^create$', views.create),
    re_path(r'^password$', views.password),
    re_path(r'^status$', views.status),
]
