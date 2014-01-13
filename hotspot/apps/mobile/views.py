from django.shortcuts import render
from django.http import HttpResponse

from hotspot.api.models import User
from hotspot.api.models import Business
from hotspot.api.models import Hotspot
from hotspot.api.models import CheckIn

import simplejson as json

def index(request):
    hotspots = []
    for hotspot in Hotspot.objects.all():
        hotspots.append({
            'name':hotspot.name,
            'LAT':hotspot.LAT,
            'LNG':hotspot.LNG,
        })

    hotspots_json = json.dumps(hotspots)
    context = {
        'hotspots': hotspots,
        'hotspots_json': hotspots_json,
    }
    return render(request, 'index.html', context)
