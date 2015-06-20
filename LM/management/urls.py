from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from management import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^setpasswd/$', views.setpasswd, name='setpasswd'),
    # url(r'^addbook/$', views.addbook, name='addbook'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^viewbook/', include('management.viewbooks_url')),
    url(r'^image/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_PATH}),
]
