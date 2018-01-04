#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from web.models import User,information,Out
from django import forms
from data import *
import django
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import time
import json
from datetime import datetime
from dateutil import tz
import pytz
admins=['zengfs@net-east.com']
#outs={"liantong":"联通","dianxin":"电信","yidong":"移动"}
do_time={"zao":["09:30","12:30"],
         "zhong":["13:30","14:30"],
         "wan":["18:30","19:30"],
         "wan1":["21:30","22:30"]
        }

class UserForm(forms.Form):
    username=forms.CharField(label="账号 ",max_length=200)
    password=forms.CharField(label="密码 ",widget=forms.PasswordInput())

def index(request):
    return render(request,'index.html')
# Create your views here.
def login(request):
    return login_mytask(request)

def login_1(request):
    if request.method=='POST':
        uf=UserForm(request.POST)
        if uf.is_valid():
            username=uf.cleaned_data['username']
            password=uf.cleaned_data['password']
            user=User.objects.filter(username=username,password=password)
            if user:
                request.session['user_id'] = user[0].id
                if user[0].groupname=="admin":
                    users=[]
                    for user1 in User.objects.all():
                        if user1.username =='admin':continue
                        users.append(user1.chinese_name)
                    return render(request,"index.html",{"outs":get_outs(user[0].groupname),"users":users})
                return render(request,"home.html",{"outs":get_outs(user[0].groupname),"username":user[0].chinese_name})
            else:
                return HttpResponseRedirect('/')
    else:
        uf=UserForm()
#        captcha=CaptchaField()
    return render(request,'login.html',{'uf':uf})

@csrf_exempt
def post_flow(request):
    flow={}
    #now=django.utils.timezone.utcnow().split(".")[0]
    now=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    #now=time.strftime('%Y-%m-%d %H:%M:%S',django.utils.timezone.utcnow())
    _time=now.split()[-1][0:5]
    if cmp(_time,do_time["zao"][1])<1 and cmp(_time,do_time["zao"][0])>-1:pass
    elif cmp(_time,do_time["zhong"][1])<1 and cmp(_time,do_time["zhong"][0])>-1:pass
    elif cmp(_time,do_time["wan"][1])<1 and cmp(_time,do_time["wan"][0])>-1:pass
    elif cmp(_time,do_time["wan1"][1])<1 and cmp(_time,do_time["wan1"][0])>-1:pass
    else:
        return render(request,'home0.html',{"title":"现在不是填报的时间"})
    _user=request.POST["user"]
    user=User.objects.get(username=_user)
    for out,out_a in get_outs(user.groupname).iteritems():
#        try:
        aa={}
        aa["flow"]=request.POST[out]
        aa["status"]=request.POST[out+"_status"]
        flow[out]=aa
        information.objects.create(user=_user,date=now,out_name=out,out=flow[out]["flow"],status=flow[out]["status"])
#        except: pass
    return render(request,'home0.html',{"title":"提交成功"})
    # return render_to_response( 'home0.html',{"title":"提交成功"},context_instance=RequestContext(request))

def get_date(request):
    if request.method == 'POST':
        form = InformationForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            date = form.cleaned_data['date']
            out=form.cleaned_data['out']
            status=form.cleaned_data['status']
            information.objects.create(user=user,date=date,out=out,status=status)
        else:
            form = InformationForm()
    return render(request, 'home.html', {'form': form})

def sort2json(aa,d,u,out):
    result={"date":d,"name":u,"out":out,"status":"正常",
            "flow1":{"date":"","num":""},
            "flow2":{"date":"","num":""},
            "flow3":{"date":"","num":""},
            "flow4":{"date":"","num":""}}
    for a in aa:
        if not a.has_key(d):continue
        if not a[d].has_key(u):continue
        if a[d][u].has_key(out):
            b=a[d][u][out]
            if cmp(b["time"],do_time["zao"][1])<1 and cmp(b["time"],do_time["zao"][0])>-1:
                result["flow1"]={"date":b["time"],"num":b["out_flow"]}
                if b["status"]==u"1":result["status"]="异常"
            elif cmp(b["time"],do_time["zhong"][1])<1 and cmp(b["time"],do_time["zhong"][0])>-1:
                result["flow2"]={"date":b["time"],"num":b["out_flow"]}
                if b["status"]==u"1":result["status"]="异常"
            elif cmp(b["time"],do_time["wan"][1])<1 and cmp(b["time"],do_time["wan"][0])>-1:
                result["flow3"]={"date":b["time"],"num":b["out_flow"]}
                if b["status"]=="1":result["status"]="异常"
            elif cmp(b["time"],do_time["wan1"][1])<1 and cmp(b["time"],do_time["wan1"][0])>-1:
                result["flow4"]={"date":b["time"],"num":b["out_flow"]}
                if b["status"]=="1":result["status"]="异常"
            else:pass
    if result["flow1"]["num"]=="" and result["flow2"]["num"]=="" and result["flow3"]["num"]=="" and result["flow4"]["num"]=="":return None
    return result

def get_json(request):
    outs_new=get_outs("admin")
    aa=[]
    bb=[]
    l_date=[]
    l_user=[]
    infos=information.objects.all()
    for info in infos:
        _date=info.date
        date=_date.split()
        user=info.user
        out_name=outs_new[info.out_name]
        out_flow=info.out
        status=info.status
        if date[0] not in l_date:l_date.append(date[0])
        if user not in l_user:l_user.append(user)
        aa.append({date[0]:{user:{out_name:{"status":status,"out_flow":out_flow,"time":date[1][0:5]}}}})
    for d in l_date:
        for u in l_user:
            for out,out_a in outs_new.iteritems():
                oo=sort2json(aa,d,u,out_a)
                if oo is not None:bb.append(oo)
    print bb
    cc=sorted(bb,key=lambda a:a['date'],reverse=True)
    print cc
    return HttpResponse(json.dumps(cc))

def add_task(request):
    if request.method=='POST':
        ID=request.session.get('user_id')
        user=User.objects.filter(id=ID)[0]
        info=request.POST['info']
        if request.POST['type']==0:Type="每日任务"
        else: Type="单次任务"
        try:
            now=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d%H%M%S')
            task.objects.create(user=user.chinese_name,IDD=now,info=info,Type=Type,status="未完成",shenpi="待审批",pingjia="-",createUserGroup=user.groupname)
            return HttpResponseRedirect('/')
        except Exception,e:
            print Exception,e
            return render(request,'home0.html',{"title":"添加任务失败，返回任务界面"})
            # return render_to_response('home0.html',{"title":"添加任务失败，返回任务界面"},context_instance=RequestContext(request))
    else:
        if request.session:
            ID=request.session.get('user_id')
            user=User.objects.filter(id=ID)
            return render(request,"add_task.html",{"username":user[0].chinese_name})
            # return render_to_response("add_task.html",{"username":user[0].chinese_name},context_instance=RequestContext(request))
        else:
            uf=UserForm()
            return render(request,'login.html',{'uf':uf})
            # return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))

def complate_task(request):
    if request.session:
        user=User.objects.filter(id=request.session.get('user_id'))
        if len(user)==1:
            IDD=request.GET['ID']
            task1=task.objects.filter(user=user[0].chinese_name,IDD=IDD)[0]
            task1.status="已完成"
            task1.save()
            return HttpResponseRedirect('/')
    uf=UserForm()
    return render(request,'login.html',{'uf':uf})
    # return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))

def del_task(request):
    if request.session:
        user=User.objects.filter(id=request.session.get('user_id'))
        if len(user)==1:
            IDD=request.GET['ID']
            task1=task.objects.filter(user=user[0].chinese_name,IDD=IDD)[0]
            if task1.createUserGroup=="admin" and user[0].groupname=="admin":
                task1.delete()
                return HttpResponseRedirect('/')
            if task1.shenpi == u"已通过" or task1.createUserGroup == "admin":
                return HttpResponseRedirect('/')
            task1.delete()
            return HttpResponseRedirect('/')
    uf=UserForm()
    return render(request,'login.html',{'uf':uf})
    # return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))
