from django.shortcuts import render
from django.http import HttpResponse

from models import User
from models import UserProfile
from models import Business
from models import Hotspot
from models import CheckIn

def docs(request):
    context = {}
    return render(request, 'docs.html', context)

# Hotspot Access

def get_all_hotspots(request):
    hotspots = Hotspot.objects.all()
    context = {'hotspots': hotspots}
    return render(request, 'hotspots.html', context)

def hotspot_by_id(request, hotspot_id):
    hotspots = Hotspot.objects.filter(id=hotspot_id)
    context = {'hotspots': hotspots}
    return render(request, 'hotspots.html', context)

def hotspot_by_name(request, hotspot_name):
    hotspots = Hotspot.objects.filter(name=hotspot_name)
    context = {'hotspots': hotspots}
    return render(request, 'hotspots.html', context)

def get_all_users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'users.html', context)

# User Access

def get_current_user(request):
    users = []
    users.append(request.user)
    context = {'users': users}
    return render(request, 'users.html', context)

def user_by_username(request, username):
    users = User.objects.filter(username=username)
    context = {'users': users}
    return render(request, 'users.html', context)

def user_by_id(request, user_id):
    users = User.objects.filter(id=user_id)
    context = {'users': users}
    return render(request, 'users.html', context)

