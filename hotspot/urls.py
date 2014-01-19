from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

import xadmin
xadmin.autodiscover()

#urlpatterns = patterns('django.views.generic.simple',('^docs[^/]$', 'redirect_to', {'url': '/docs/index.html'})),

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hotspot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT, 'show_indexes':True}),
    #url(r'^xadmin/', include(xadmin.site.urls)),

    # Other URLs
    url(r'^$',          include('hotspot.apps.mobile.urls')),

    url(r'^mobile/',    include('hotspot.apps.mobile.urls')),
    url(r'^api/',       include('hotspot.api.urls')),
    url(r'^accounts/',  include('allauth.urls'))
)

