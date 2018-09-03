from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^password$', views.update_password),
    re_path(r'^username$', views.update_username),
    re_path(r'^profile$', views.update_profile),
]
