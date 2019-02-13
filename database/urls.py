from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^createuser$', views.CreateUser),
    re_path(r'^createdatabase$', views.CreateDatabase),
    re_path(r'^grantuser$', views.GrantUser),
]
