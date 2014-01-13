from django.shortcuts import render
from django.http import HttpResponse


from models import User
from models import UserProfile
from models import Business
from models import Hotspot
from models import CheckIn

def docs(request):
    return HttpResponse("api responds with: api docs")

def hotspot_by_id(request, hotspot_id):
    return HttpResponse("api responds with: hotspot/%s" % hotspot_id)

def hotspot_by_name(request, hotspot_name):
    return HttpResponse("api responds with: hotspot/%s" % hotspot_name)

def user(request, username):
    return HttpResponse("api responds with: user/%s" % username)
