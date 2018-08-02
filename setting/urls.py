from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^password$', views.modify_password),
    re_path(r'^username$', views.modify_username),
]
