from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hotspot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Other URLs
    url(r'^$',          include('hotspot.apps.desktop.urls')),
    #url(r'^.*.html',    include('hotspot.apps.desktop.urls')),

    url(r'^mobile/',    include('hotspot.apps.mobile.urls')),
    url(r'^api/',       include('hotspot.api.urls')),
    url(r'^accounts/',  include('allauth.urls')),
)
