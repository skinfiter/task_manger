#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from device_management.models import device_info
from web.models import User
from faults_record.models import point as POINT
from django.template import RequestContext
import time
from datetime import datetime
from dateutil import tz
import pytz

#USERS=[1,2,3,4,5,6]

def device_lists(request):
    ID=request.session.get("user_id")
#    if ID not in USERS: return HttpResponseRedirect('/')
    devices=device_info.objects.all()
    return render_to_response("device_list.html",{"devices":devices},context_instance=RequestContext(request))

def add_device_info(request):
    if request.method=="GET":
        points=POINT.objects.all()
        return  render_to_response("add_device_info.html",{"points":points},context_instance=RequestContext(request))
    elif request.method=="POST":
        try:
            ID=request.session.get('user_id')
            user=User.objects.filter(id=ID)
            create_date=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
            brands=request.POST["brands"]
            MODEL=request.POST["MODEL"]
            serial_numbers=request.POST["serial_numbers"]
            cpu=request.POST["cpu"]
            ram=request.POST["ram"]
            storage=request.POST["storage"]
            nic=request.POST["nic"]
            count=int(request.POST["count"])
            attri=request.POST["attri"]
            point=POINT.objects.filter(id=request.POST["point"])[0].point_name
            usage=request.POST["usage"]
            info=request.POST["info"]
            create_user=user[0].chinese_name
            device_info.objects.create(create_date=create_date,brands=brands,MODEL=MODEL,serial_numbers=serial_numbers,cpu=cpu,ram=ram,storage=storage,nic=nic,count=count,attri=attri,point=point,usage=usage,info=info,create_user=create_user)
            return HttpResponseRedirect("/device_manager")
        except Exception,e:
            print Exception,e
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
