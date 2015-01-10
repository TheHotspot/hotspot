from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.db import IntegrityError

import simplejson as json
import datetime

from rest_framework import viewsets, serializers, permissions, renderers
from rest_framework.decorators import link

### v3 REST Framework API

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
