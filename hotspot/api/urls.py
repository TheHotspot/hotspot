from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    # TODO: eventually make this go to API docs
    url(r'^$', views.docs, name='docs'),

    # Full Hotspot Listing
    url(r'^hotspots/$', views.get_all_hotspots, name='hotspots'),

    # Hotspot by ID
    url(r'^hotspot/(?P<hotspot_id>\d+)(/||$)', views.hotspot_by_id, name='hotspot'),

    # Hotspot by name
    url(r'^hotspot/(?P<hotspot_name>\D.*[^/])(/||$)', views.hotspot_by_name, name='hotspot'),

    # User by username
    url(r'^user/(?P<username>.*)(/||$)', views.user, name='user'),
)
