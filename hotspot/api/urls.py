from django.conf.urls import patterns, include, url

from views import GenericViewSet, GenericSerializer

from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

import models

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'hotspots': reverse('hotspot-list', request=request, format=format),
        'businesses': reverse('business-list', request=request, format=format),
        'checkins': reverse('checkin-list', request=request, format=format),
    })


urlpatterns = patterns('',
    url(r'^$', api_root),
    url(r'^users/$', GenericViewSet(models.User, ('id', 'first_name', 'last_name', 'email', 'telephone')).as_view({"get": "list"}), name='user-list'),
    url(r'^hotspots/$', GenericViewSet(models.Hotspot, ('id', 'name', 'LAT', 'LNG', 'nickname', 'capacity', 'telephone')).as_view({"get": "list"}), name='hotspot-list'),
    url(r'^businesses/$', GenericViewSet(models.Business, ('id', 'name', 'logo')).as_view({"get": "list"}), name='business-list'),
    url(r'^checkins/$', GenericViewSet(models.CheckIn, ('id', 'time_in', 'time_out')).as_view({"get": "list"}), name='checkin-list'),

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
)
