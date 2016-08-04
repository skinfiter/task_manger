#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from web.models import User,information,Out
from django import forms
from django.template import RequestContext
from data import *
from datetime import datetime
from dateutil import tz
import pytz,time

class UserForm(forms.Form):
    username=forms.CharField(label="账号 ",max_length=200)
    password=forms.CharField(label="密码 ",widget=forms.PasswordInput())

def login_mytask(request):
    if request.method=='POST':
        uf=UserForm(request.POST)
        if uf.is_valid():
            username=uf.cleaned_data['username']
            password=uf.cleaned_data['password']
            user=User.objects.filter(username=username,password=password)
            if user:
                request.session['user_id'] = user[0].id
                # if user[0].groupname=="admin":
                    # users=[]
                    # for user1 in User.objects.all():
                        # if user1.groupname=="admin":continue
                    # task_info=get_tasks()
                    # return render_to_response("my__tasks.html",{"task_info":task_info,"username":user[0].chinese_name},context_instance=RequestContext(request))
                # task_info=get_tasks(user[0].chinese_name)
                task_info=sorted(task.objects.filter(user=user[0].chinese_name),key=lambda a:a.IDD,reverse=True)
                task_info=sorted(task_info,key=lambda a:a.status,reverse=True)
                return render_to_response("my_tasks.html",{"task_info":task_info,"username":user[0].chinese_name,"group":user[0].groupname},context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect('/')
    else:
        if request.session:
            ID=request.session.get('user_id')
            user=User.objects.filter(id=ID)
            if len(user)==1:
            #    task_info=get_tasks(user[0].chinese_name)
                task_info=sorted(task.objects.filter(user=user[0].chinese_name),key=lambda a:a.IDD,reverse=True)
                task_info=sorted(task_info,key=lambda a:a.status,reverse=True)
                return render_to_response("my_tasks.html",{"task_info":task_info,"username":user[0].chinese_name,'group':user[0].groupname},context_instance=RequestContext(request))
    uf=UserForm()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))

def shenpi(request):
    if request.session:
        ID=request.session.get('user_id')
        user=User.objects.filter(id=ID)[0]
        if user.groupname=='admin':
            try:
                Uname=request.GET['user']
                tasks=task.objects.filter(status="已完成",shenpi="待审批",user=Uname)
            except:
                tasks=task.objects.filter(status="已完成",shenpi="待审批")
            task_info=[]
            for task1 in tasks:
                task_info.append({'id':task1.id,'IDD':task1.IDD,'info':task1.info,'type':task1.Type,'status':task1.status,'shenpi':task1.shenpi,'user':task1.user})
            return render_to_response("manger.html",{"task_info":task_info,"username":user.chinese_name},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def logout(request):
    try:
        del request.session['user_id']
    except:pass
    return HttpResponseRedirect('/')
    # uf=UserForm()
    # return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))

def bypass(request):
    if request.session:
        ID=request.session.get('user_id')
        user=User.objects.filter(id=ID)
        if len(user)==1 and user[0].groupname=='admin':
            IDD=request.POST['id']
            task1=task.objects.filter(id=IDD)[0]
            task1.shenpi="已通过"
            task1.pingjia=request.POST['pingjia']
            task1.save()
            return HttpResponseRedirect('/shenpi')
    return HttpResponseRedirect('/')

def task_per(request):
    if request.session:
        try:
            ID=request.session.get('user_id')
            username=User.objects.filter(id=ID)[0].chinese_name
            users=[]
            for user in User.objects.all():
                if user.groupname=="admin":continue
                users.append(user)
            tasks=task.objects.filter(status="未完成")
            # if len(tasks)>10:tasks=tasks[0:10]
            return render_to_response('task_list.html',{"users":users,"tasks":tasks,"username":username},context_instance=RequestContext(request))
        except:pass
    return HttpResponseRedirect('/')

def show_per_all(request):
    if request.session:
        try:
            Uname=request.GET['user']
            tasks=task.objects.filter(user=Uname)
            tasks=sorted(tasks,key=lambda a:a.IDD,reverse=True)
            tasks=sorted(tasks,key=lambda a:a.status,reverse=True)
            user=User.objects.filter(chinese_name=Uname)[0]
            ID=request.session.get('user_id')
            cuser=User.objects.filter(id=ID)[0]
            # print cuser.groupname
            return render_to_response("task_per_all.html",{"task_info":tasks,"user":user,"cuser":cuser},context_instance=RequestContext(request))
        except Exception,e:
            print Exception,e
            pass
    return HttpResponseRedirect('/')

def xiafa_task(request):
    if request.session:
        ID=request.session.get("user_id")
        user=User.objects.filter(id=ID)[0]
        if user.groupname=="admin":
            print request.method
            if request.method=="GET":
                users=User.objects.exclude(groupname="admin")
                return render_to_response('xiafa_task.html',{"users":users,"cuser":user},context_instance=RequestContext(request))
            elif request.method=="POST":
                now=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d%H%M%S')
                Uname=request.POST['user']
                info=request.POST['info']
                if request.POST['type']==0:Type="每日任务"
                else: Type="单次任务"
                task.objects.create(user=Uname,IDD=now,info=info,Type=Type,status="未完成",shenpi="待审批",pingjia="-",createUserGroup="admin")
            else:pass
        else:
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')
    # return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))

def person(request):
    try:
        ID=request.session.get("user_id")
        user=User.objects.filter(id=ID)[0]
        if request.method=="GET":
            return render_to_response('person_info.html',{"user":user},context_instance=RequestContext(request))
        elif request.method=="POST":
            user.chinese_name=request.POST["chinese_name"]
            user.photo_url=request.POST['photo_url']
            user.save()
            return render_to_response('person_info.html',{"user":user,"TYPE":"1"},context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')
