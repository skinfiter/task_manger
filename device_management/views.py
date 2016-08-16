#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from device_management.models import device_info
from django import forms
import django
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import time
import json
from datetime import datetime
from dateutil import tz
import pytz

USERS=[1,]

def device_lists(request):
    ID=request.session.get("user_id")
    if ID not in USERS: return HttpResponseRedirect('/')
    devices=device_info.objects.all()
    return render_to_response("device_list.html",{"devices":devices},context_instance=RequestContext(request))
