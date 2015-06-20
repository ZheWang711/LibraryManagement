__author__ = 'WangZhe'
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from management import views
urlpatterns = [
    # url(r'$type=(?P<record_type>\D+)/$', views.viewbook, name='viewbookByType'),
    # url(r'^type=(?P<record_type>\D+)/$', views.viewbook, name='viewByPage'),
    url(r'^$', views.viewbook, name='viewbook'),
    url(r'^detail/id=(?P<record_id>\d+)/$', views.detail, name='detail'),
    ]