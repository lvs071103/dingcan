from django.conf.urls import patterns, url
from dc_manager import views
# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'^$', views.dingcan_list, name='dingcan_list'),
    url(r'^new$', views.dingcan_create, name='dingcan_new'),
    url(r'^edit/(?P<pk>\d+)$', views.dingcan_update, name='dingcan_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.dingcan_delete, name='dingcan_delete'),
    url(r'^admin_display/$', views.admin_display, name='admin_display')
) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
  #            static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)