from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.user),
    url(r'^admin$', views.admin)
]