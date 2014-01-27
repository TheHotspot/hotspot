from django.shortcuts import render
from django.http import HttpResponse

from hotspot.api.models import User
from hotspot.api.models import Business
from hotspot.api.models import Hotspot
from hotspot.api.models import CheckIn

import simplejson as json

device = "mobile"

def index(request):
    hotspots = []
    for hotspot in Hotspot.objects.all():
        hotspots.append({
            'id':hotspot.id,
            'name':hotspot.name,
            'LAT':hotspot.LAT,
            'LNG':hotspot.LNG,
            'logo':hotspot.logo,
            'description':hotspot.description,
            'address':hotspot.address,
            'nickname':hotspot.nickname,
            'capacity':hotspot.capacity,
            'website':hotspot.website,
            'telephone':hotspot.telephone,
        })

    hotspots_json = json.dumps(hotspots)
    checkins = CheckIn.checkins_checkedin().count()
    context = {
        'hotspots': hotspots,
        'checkins': checkins,
        'hotspots_json': hotspots_json,
        'device': device,
    }
    return render(request, 'mobile/index.html', context)
