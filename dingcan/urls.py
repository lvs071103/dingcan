from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dingcan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dingcan/', include('dc_manager.urls')),
) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
  #            static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
