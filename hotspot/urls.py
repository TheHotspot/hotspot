from django.conf.urls import patterns, include, url
from django.conf import settings


if settings.USE_XADMIN:
    import xadmin
    xadmin.autodiscover()
else:
    from django.contrib import admin
    admin.autodiscover()

urlpatterns = patterns('',
    # Admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Other URLs
    url(r'^mobile/',    include('hotspot.apps.mobile.urls')),
    url(r'^api/',       include('hotspot.api.urls')),
    url(r'^auth/',      include('allauth.urls')),
    url(r'^$',          include('hotspot.apps.mobile.urls')),
)

if settings.USE_XADMIN:
    urlpatterns += patterns('',
        url(r'^admin/', include(xadmin.site.urls)),
    )
else:
    urlpatterns += patterns('',
        url(r'^admin/',     include(admin.site.urls)),
    )

if settings.SERVE_STATIC_WITH_DJANGO:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^docs/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'hotspot/docs/_build/html', 'show_indexes':True}),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
    
