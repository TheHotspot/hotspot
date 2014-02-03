from django.conf.urls import patterns, include, url

from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter

import views
import hotspot.api.models as models

router = DefaultRouter()
router.register(r'users', views.GenericViewSet(models.User, ('id', 'get_full_name', 'email', 'gender', 'status', 'birthdate')))
router.register(r'hotspots', views.GenericViewSet(models.Hotspot, ('id', 'name', 'LAT', 'LNG', 'nickname', 'capacity', 'telephone')))
router.register(r'businesses', views.GenericViewSet(models.Business, ('id', 'name', 'logo')))
router.register(r'checkins', views.GenericViewSet(models.CheckIn, ('id', 'time_in', 'time_out')))

### v3 REST Framework API

urlpatterns = patterns('',
    url(r'', include(router.urls)),
)
