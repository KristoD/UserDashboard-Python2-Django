from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^users/show/(?P<id>\d+)$', views.show),
    url(r'^users/edit/(?P<id>\d+)$', views.edit),
    url(r'^edit/(?P<action>\w+)$', views.edit_process),
    url(r'^process/(?P<action>\w+)$', views.process),
    url(r'^users/new$', views.new),
    url(r'^users/destroy/(?P<id>\d+)$', views.destroy),
]