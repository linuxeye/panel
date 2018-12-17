from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^add$', views.AddDatabase),
    re_path(r'^create$', views.CreateDatabase),
]
