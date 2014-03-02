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

@csrf_exempt
def docs(request):
    version = 2
    context = {'version': version}
    return render(request, 'api/docs.html', context)

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
                    "tolerance":        str(hotspot.tolerance),
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
def scan(request):
    hotspot_id = get_parameter(request, 'id', '')
    session = get_parameter(request, 'session', '')   # horrible, django doesnt use this auth method, only cookies allowed

    response = {"status":"ERROR-SCAN-FAILURE","scan_id": 0, "user_stats":{"stats_total_scans":0, "stats_distinct_hotspot_scans":0}}

    if request.user.is_authenticated():
        user = request.user
        if hotspot_id:
            hotspot = Hotspot.objects.get(id=hotspot_id)
            try:
                response["scan_id"] = user.checkin(hotspot).id
                response["status"] = "SUCCESS"
            except:
                pass

        response["user_stats"]["stats_total_scans"] = user.checkins().count()
        response["user_stats"]["stats_distinct_hotspot_scans"] = user.hotspots_visited().count()

    else:
        response["status"] = "ERROR-NO-AUTH"

    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def locate(request):
    lat = get_parameter(request, 'lat', '')
    lng = get_parameter(request, 'lng', '')
    tol = get_parameter(request, 'tolerance', '')

    response = {"status":"ERROR-NO-RESULTS","hotspot": False}

    if lat and lng:
        hotspot = Hotspot.raw_search_by_radius(lat, lng, radius=1, limit=10)
        if hotspot:
            response["status"] = "SUCCESS"
            response["hotspot"] = hotspot_json(hotspot[0])
        else:
            response["status"] = "ERROR-NO-RESULTS"


    return HttpResponse(json.dumps(response), content_type="application/json")
