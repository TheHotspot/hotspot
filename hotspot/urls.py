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
    #   r'^admin/',      -->     Django Admin or Xadmin (see below)
    #   r'^docs/',       -->     sphinx docs   (see below)
    url(r'^docs/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'hotspot/docs/_build/html', 'show_indexes':True}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Website
    url(r'^$',          include('hotspot.apps.web.urls')),
    url(r'^mobile/',    include('hotspot.apps.web.urls')),
    url(r'^dashboard/', include('hotspot.apps.dashboard.urls')),

    # Authentication (pages with passwords)
    url(r'^auth/',      include('allauth.urls'), {'SSL':True}),
    url(r'^accounts/',  include('allauth.urls'), {'SSL':True}),

    # APIs
    url(r'^public-api/',include('hotspot.public-api.urls')),
    url(r'^pubapi/',    include('hotspot.public-api.urls')),
    url(r'^api/v2/',    include('hotspot.api.urls')),
    url(r'^api/v1/',    include('hotspot.legacy-api.urls')),
    url(r'^api/',       include('hotspot.legacy-api.urls')),
)

if settings.USE_XADMIN:
    urlpatterns += patterns('',
        url(r'^admin/', include(xadmin.site.urls)),
        url(r'^xadmin/', include(xadmin.site.urls)),
    )
else:
    urlpatterns += patterns('',
        url(r'^admin/',     include(admin.site.urls)),
    )

# serve the static files with django instead of apache, useful for wsgi debugging (dont use in production!)
if settings.SERVE_STATIC_WITH_DJANGO:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

