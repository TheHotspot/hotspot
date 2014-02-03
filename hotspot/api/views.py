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

from models import User
from models import Business
from models import Hotspot
from models import CheckIn

### Favored API for Hotspot-made apps to access internal data

def get_parameter(request, key, default=""):
    get = request.GET.get(key, False)
    post = request.POST.get(key, False)
    if get:
        return get
    if post:
        return post
    else:
        return default

def hotspot_json(hotspot, distance=0):
    if hotspot:
        return {
                    "hotspot_id":       str(hotspot.id),
                    "name":             hotspot.name,
                    "description":      hotspot.description,
                    "nickname":         hotspot.nickname,
                    "website":          hotspot.website,
                    "phone_number":     hotspot.telephone,
                    "latitude":         str(hotspot.LAT),
                    "longitude":        str(hotspot.LNG),
                    "full_address":     hotspot.address,
                    "distance":         str(distance),
                    "categories":       None,
                    "stats_total_scans": str(hotspot.checkins().count()),
                    "stats_current_scanned": str(hotspot.checkins_checkedin().count()),
                    "stats_male_scans": "0",
                    "stats_female_scans": "0"
                }
    else:
        return {}

@csrf_exempt
def docs(request):
    version = 1
    context = {'version': version}
    return render(request, 'api/docs.html', context)
