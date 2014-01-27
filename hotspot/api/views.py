from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from rest_framework import viewsets, serializers, permissions, renderers
from rest_framework.decorators import link

from models import User
from models import Business
from models import Hotspot
from models import CheckIn

from django.db import models

### v2 REST Framework API

def GenericSerializer(imodel, ifields=('id', '__unicode__')):
    class Serializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = imodel
            fields = ifields
    return Serializer

def GenericViewSet(model, ifields=('id', '__unicode__')):
    class ViewSet(viewsets.ModelViewSet):
        queryset = model.objects.all()
        serializer_class = GenericSerializer(model, ifields)
    return ViewSet


### v1 API for iPhone app backwards-compatibility

def docs(request):
    version = 1
    context = {'version': version}
    return render(request, 'api/docs.html', context)

# Hotspot Access

def get_all_hotspots(request):
    hotspots = Hotspot.objects.all()
    context = {'hotspots': hotspots}
    return render(request, 'api/hotspots.html', context)

def hotspot_by_id(request, hotspot_id):
    hotspots = Hotspot.objects.filter(id=hotspot_id)
    context = {'hotspots': hotspots}
    return render(request, 'api/hotspots.html', context)

def hotspot_by_name(request, hotspot_name):
    hotspots = Hotspot.objects.filter(name=hotspot_name)
    context = {'hotspots': hotspots}
    return render(request, 'api/hotspots.html', context)

@csrf_exempt
def hotspots_by_distance(request):
    lat = request.GET.get('lat', '')
    lng = request.GET.get('lng', '')
    rad = request.GET.get('distance', '')

    if lat and lng and rad:
        hotspots = [ x for x in Hotspot.search_by_radius(lat,lng,rad) ]
        if hotspots:
            context = {'status':"SUCCESS",
                       'hotspots': hotspots}
            return render(request, 'api/hotspots.html', context)
        else:
            context = {'status': 'ERROR-NO-RESULTS'}
            return render(request, 'api/error.html', context)
    else:
        context = {'status': 'ERROR-INVALID-INPUT'}
        return render(request, 'api/error.html', context)


def get_all_users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'api/users.html', context)

# User Access

def get_current_user(request):
    users = []
    users.append(request.user)
    context = {'users': users}
    return render(request, 'api/users.html', context)

def user_by_username(request, username):
    users = User.objects.filter(username=username)
    context = {'users': users}
    return render(request, 'api/users.html', context)

def user_by_id(request, user_id):
    users = User.objects.filter(id=user_id)
    context = {'users': users}
    return render(request, 'api/users.html', context)
