from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sensor/(?P<sensor_file_system_location>[\-0-9]+)/$', views.detail, name='detail'),
]