from django.conf.urls import patterns, include, url

import views

from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter

import hotspot.api.models

### Legacy API for iPhone & Android app backwards-compatibility

urlpatterns = patterns('',
    url(r'^$', views.docs),
    url(r'^register', views.register, {'SSL':True}),
    url(r'^oauth', views.oauth, {'SSL':True}),
    url(r'^auth', views.auth, {'SSL':True}),
    url(r'^search_top', views.search),
    url(r'^search', views.search),
    url(r'^hotspot', views.hotspot_lookup),
    url(r'^scan_out', views.scan_out),
    url(r'^scan', views.scan),
    url(r'^history', views.history),
)
