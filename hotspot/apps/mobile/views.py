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

    profile_img = "http://vpn.nicksweeting.com/images/up.gif"
    if request.user.is_authenticated():
        socialaccount = request.user.socialaccount_set.filter(provider='facebook')
        if socialaccount:
            profile_img = socialaccount[0].get_avatar_url()
        
    context = {
        'hotspots': hotspots,
        'checkins': checkins,
        'hotspots_json': hotspots_json,
        'device': device,
        'profile_img': profile_img,
    }
    return render(request, 'mobile/index.html', context)
