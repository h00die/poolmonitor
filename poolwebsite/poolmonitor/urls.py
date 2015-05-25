from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sensor/(?P<sensor_file_system_location>[\-0-9a-f]+)/$', views.detail, name='detail'),
    url(r'^sensor/add/$', views.SensorCreate.as_view(), name='create'),
    url(r'^sensor/update/(?P<pk>[\-0-9]+)/$', views.SensorUpdate.as_view(), name='edit'),
    url(r'^sensor/delete/(?P<pk>[\-0-9]+)/$', views.SensorDelete.as_view(), name='delete'),
    url(r'^graph/$', views.graph, name='graph'),
    url(r'^chart/$', views.chart, name='chart'),
]