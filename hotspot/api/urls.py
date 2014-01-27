from django.conf.urls import patterns, include, url

import views

from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter

import models

router = DefaultRouter()
router.register(r'users', views.GenericViewSet(models.User, ('id', 'get_full_name', 'email', 'gender', 'status', 'birthdate')))
router.register(r'hotspots', views.GenericViewSet(models.Hotspot, ('id', 'name', 'LAT', 'LNG', 'nickname', 'capacity', 'telephone')))
router.register(r'businesses', views.GenericViewSet(models.Business, ('id', 'name', 'logo')))
router.register(r'checkins', views.GenericViewSet(models.CheckIn, ('id', 'time_in', 'time_out')))

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

    # # API Documentation
    # url(r'^$', views.docs, name='docs'),

    # # Authentication
    # url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),


    # # Full Hotspot Listing
    # url(r'^hotspots/$', views.get_all_hotspots, name='hotspots'),

    # # Hotspot by ID
    # url(r'^hotspot/(?P<hotspot_id>\d+)(/||$)', views.hotspot_by_id, name='hotspot'),

    # # Hotspot by name
    # url(r'^hotspot/(?P<hotspot_name>\D.*[^/])(/||$)', views.hotspot_by_name, name='hotspot'),



    # # Full User Listing
    # url(r'^users/$', views.get_all_users, name='users'),

    # # Currently logged in user
    # url(r'^user/$', views.get_current_user, name='user'),

    # # User by ID
    # url(r'^user/(?P<user_id>\d+)(/||$)', views.user_by_id, name='user'),

    # # User by username
    # url(r'^user/(?P<username>\D.*[^/])(/||$)', views.user_by_username, name='user'),

    # Rest Framework API
    url(r'^v2/', include(router.urls)),
)
