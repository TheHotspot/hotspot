from django.conf.urls import patterns, include, url

from views import UserViewSet

from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
    })


urlpatterns = patterns('',
    url(r'^$', api_root),
    url(r'^users/$', UserViewSet.as_view({"get": "list"}), name='user-list'),

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
