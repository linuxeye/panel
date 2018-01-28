from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^password$', views.modify_password),
    url(r'^username$', views.modify_username),
]
