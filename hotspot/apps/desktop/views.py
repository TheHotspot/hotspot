from django.shortcuts import render
from django.http import HttpResponse

from hotspot.api.models import User
from hotspot.api.models import Business
from hotspot.api.models import Hotspot
from hotspot.api.models import CheckIn

def index(request):
    hotspots = Hotspot.objects.all()
    context = {'hotspots': hotspots}
    return render(request, 'hotspots.html', context)
