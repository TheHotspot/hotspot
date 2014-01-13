from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib import admindocs
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hotspot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Admin URLs
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin/doc/', include(admindocs.site.urls)),


    # Other URLs
    url(r'^accounts/', include('allauth.urls')),
)
