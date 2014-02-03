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

from django.db import models

### Legacy API for iPhone & Android app backwards-compatibility

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

def scan_json(checkin, current=-1):
    if checkin:
        if current == -1:
            current = int(checkin.is_checkedin())
        return {
                    "scan_id":       str(checkin.id),
                    "hotspot_id":    str(checkin.hotspot.id),
                    "scan_date":     str(checkin.time_in),
                    "current":       str(current),
                }
    else:
        return {}

@csrf_exempt
def register(request, SSL=True):
    email = get_parameter(request, 'email', '')
    password = get_parameter(request, 'password', '')
    name = get_parameter(request, 'name', '')
    gender = get_parameter(request, 'gender', '')
    status = get_parameter(request, 'status', '')
    birthdate = get_parameter(request, 'birthdate', '')

    response = {"status":"ERROR-FAILED-REGISTRATION"}

    if email and password and birthdate:
        birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d').date()
        valid = datetime.date.today()-datetime.timedelta(6574)

        if birthdate > valid:
            response["status"] = "ERROR-INVALID-BIRTHDATE"
        else:
            try:
                newuser = User( username=email, 
                                password=password, 
                                email=email, 
                                gender=gender,
                                status=status,
                                first_name=name.split(" ")[0], 
                                last_name=" ".join(name.split(" ")[1:]), 
                                birthdate=birthdate)
                newuser.save()
                response["user_id"] = newuser.id
                response["status"] = "SUCCESS"
            except IntegrityError as e:
                response["status"] = "ERROR-EMAIL-TAKEN"
                response["error-details"] = str(e[1])

    return HttpResponse(json.dumps(response), content_type="application/json")  

@csrf_exempt
def auth(request, SSL=True):
    email = get_parameter(request, 'e', '')
    passhash = get_parameter(request, 'h', '')

    response = {"status":"ERROR-INVALID-AUTH",
                "session":"",
                "user_id":"",
                "is_manager":"",
                "join_date":"",
                "name":"",
                "maritial_status":"",
                "gender":""}

    if email and passhash:
        username = User.objects.filter(email=email)[0].username
        user = authenticate(username=username, password=passhash)

        if user is not None:
            if user.is_active:
                login(request, user)
                response["status"] = "AUTHENTICATED"

                response["user_id"] = str(user.id)
                response["is_manager"] = str(int(user.is_admin()))
                response["join_date"] = str(user.date_joined)
                response["name"] = user.get_full_name()
                response["maritial_status"] = "1"
                response["gender"] = "M"

            else:
                response["status"] = "ERROR-USER-BANNED"
    
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def search(request):
    lat = get_parameter(request, 'lat', '')
    lng = get_parameter(request, 'lng', '')
    rad = get_parameter(request, 'distance', '10')
    limit = get_parameter(request, 'limit', '200')

    response = {"status":"ERROR-INVALID-INPUT","results": []}

    if lat and lng and rad:
        response["status"] = "SUCCESS"
        for idx, hotspot in enumerate(Hotspot.search_by_radius(lat,lng,rad,limit)):
            response["results"].append(hotspot_json(hotspot, distance=idx))
        if not response["results"]:
            response["status"] = "ERROR-NO-RESULTS"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def hotspot_lookup(request):
    hotspot_id = get_parameter(request, 'id', '')

    response = {"status":"ERROR-NO-HOTSPOT","hotspot": 0}

    if hotspot_id:
        try:
            hotspot = Hotspot.objects.get(id=hotspot_id)
            response["status"] = "SUCCESS"
            response["hotspot"] = hotspot_json(hotspot)
        except:
            pass
    
    return HttpResponse(json.dumps(response), content_type="application/json")

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
def scan_out(request):
    """
    check the user out of anywhere they're checked in
    """
    session = get_parameter(request, 'session', '')   # horrible, django doesnt use this auth method, only cookies allowed

    response = {"status":"ERROR-NO-AUTH"}

    if request.user.is_authenticated():
        user = request.user
        user.checkout()
        response = {"status":"SUCCESS"}

    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def history(request):
    session = get_parameter(request, 'session', '')
    limit = get_parameter(request, 'limit', '20')

    response = {"status":"ERROR-NO-AUTH","history": []}

    if request.user.is_authenticated():
        user = request.user
        response["status"] = "SUCCESS"
        hascurrrent = 0
        for checkin in user.checkins(records=limit, sort_key='time_in'):
            if checkin.is_checkedin() and not hascurrrent:
                hascurrrent = 1
                response["history"].append(scan_json(checkin, current=1))
            else:
                response["history"].append(scan_json(checkin, current=0))
    
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def oauth(request, SSL=True):
    provider = get_parameter(request, 'provider', 'facebook')
    access_token = get_parameter(request, 'access_token', '')

    response = {"status":"ERROR-OAUTH-EXCEPTION",
                "session":"",
                "user_id":"",
                "is_manager":"",
                "join_date":"",
                "name":"",
                "maritial_status":"",
                "gender":""}

    if access_token:
        user = authenticate(token=access_token)
        if user is not None:
            if user.is_active:
                login(request, user)
                response["status"] = "AUTHENTICATED"
                response["user_id"] = str(user.id)
                response["is_manager"] = str(int(user.is_admin()))
                response["join_date"] = str(user.date_joined)
                response["name"] = user.get_full_name()
                response["maritial_status"] = "1"
                response["gender"] = "M"

            else:
                response["status"] = "ERROR-USER-BANNED"
    
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def docs(request):
    version = 1
    context = {'version': version}
    return render(request, 'legacy-api/docs.html', context)
