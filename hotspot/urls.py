from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

import xadmin
xadmin.autodiscover()

urlpatterns = patterns('',
    # Admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT, 'show_indexes':True}),
#    url(r'^xadmin/', include(xadmin.site.urls)),

    # Other URLs
    url(r'^mobile/',    include('hotspot.apps.mobile.urls')),
    url(r'^api/',       include('hotspot.api.urls')),
    url(r'^accounts/',  include('allauth.urls')),
    url(r'^account/',	include('allauth.urls')),
    url(r'^$',          include('hotspot.apps.mobile.urls')),

)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

def show_toolbar(request):
    if request.user and request.user.username == "nick" or request.user.username == "nikisweeting":
        return True
    return False
