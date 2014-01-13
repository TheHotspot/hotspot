from django.shortcuts import render
from django.http import HttpResponse


from models import User
from models import UserProfile
from models import Business
from models import Hotspot
from models import CheckIn

def docs(request):
    return HttpResponse("api responds with: api docs")

def get_all_hotspots(request):
    hotspots = Hotspot.objects.all()
    context = {'hotspots': hotspots}
    return render(request, 'response.html', context)

def hotspot_by_id(request, hotspot_id):
    hotspots = Hotspot.objects.filter(id=hotspot_id)
    context = {'hotspots': hotspots}
    return render(request, 'response.html', context)

def hotspot_by_name(request, hotspot_name):
    hotspots = Hotspot.objects.filter(name=hotspot_name)
    context = {'hotspots': hotspots}
    return render(request, 'response.html', context)

def user(request, username):
    return HttpResponse("api responds with: user/%s" % username)
