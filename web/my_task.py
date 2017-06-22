#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from web.models import User,information,Out
from django import forms
from django.template import RequestContext
from data import *
import datetime
from dateutil import tz
import pytz,time
from download import *
from django.http import StreamingHttpResponse

class UserForm(forms.Form):
    username=forms.CharField(label="账号 ",max_length=200)
    password=forms.CharField(label="密码 ",widget=forms.PasswordInput())

def login_mytask(request):
    week_c=int(time.strftime("%w"))
    tasks=[]
    today=datetime.date.today()
    if request.method=='POST':                     ###登陆部分
        uf=UserForm(request.POST)
        if uf.is_valid():
            username=uf.cleaned_data['username']
            password=uf.cleaned_data['password']
            user=User.objects.filter(username=username,password=password)
            if user:
                request.session['user_id'] = user[0].id
                weeks=0
                s_Ddate=(today-datetime.timedelta(days=(week_c-1+7*weeks))).strftime('%Y-%m-%d')
                e_Ddate=(today-datetime.timedelta(days=(week_c-7+7*weeks))).strftime('%Y-%m-%d')
                Ddate=s_Ddate+" -- "+e_Ddate
                for i in range(1,8):
                    _date=(today-datetime.timedelta(days=(week_c-i+7*weeks))).strftime('%Y%m%d')
                    tasks.extend(task.objects.filter(user=user[0].chinese_name,IDD__contains=_date))
                task_info=sorted(tasks,key=lambda a:a.IDD,reverse=True)
                task_info=sorted(task_info,key=lambda a:a.status,reverse=True)
                data_aa={"username":user[0].chinese_name,'group':user[0].groupname,"task_info":task_info,"ago_week":weeks+1,"week":weeks,"next_week":weeks-1,"date":Ddate}
                return render(request,'my_tasks.html',data_aa)
                # task_info=sorted(task.objects.filter(user=user[0].chinese_name),key=lambda a:a.IDD,reverse=True)
                # task_info=sorted(task_info,key=lambda a:a.status,reverse=True)
                # return render_to_response("my_tasks.html",{"task_info":task_info,"username":user[0].chinese_name,"group":user[0].groupname},context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect('/')
    else:                        ###个人任务部分
        if request.session:
            ID=request.session.get('user_id')
            user=User.objects.filter(id=ID)
            if len(user)==1:
            #    task_info=get_tasks(user[0].chinese_name)
                try:
                    weeks=int(request.GET['ago'])
                except:
                    weeks=0
                s_Ddate=(today-datetime.timedelta(days=(week_c-1+7*weeks))).strftime('%Y-%m-%d')
                e_Ddate=(today-datetime.timedelta(days=(week_c-7+7*weeks))).strftime('%Y-%m-%d')
                Ddate=s_Ddate+"--"+e_Ddate
                for i in range(1,8):
                    _date=(today-datetime.timedelta(days=(week_c-i+7*weeks))).strftime('%Y%m%d')
                    tasks.extend(task.objects.filter(user=user[0].chinese_name,IDD__contains=_date))
                task_info=sorted(tasks,key=lambda a:a.IDD,reverse=True)
                task_info=sorted(task_info,key=lambda a:a.status,reverse=True)
                try:
                    if request.GET['download']=='true':
                        task_tables=[['IDD','日期'],['info','描述'],['Type','类型'],['status','进度'],['shenpi','审批'],['pingjia','评价']]
                        file_name="我的任务"+Ddate+'.xlsx'
                        return createdownloadfile(task_tables,task_info,file_name)
                except Exception,e:
                    print Exception,e
                    pass
                #return render_to_response('my_tasks.html',{"username":user[0].chinese_name,'group':user[0].groupname,"task_info":task_info,"ago_week":weeks+1,"week":weeks,"next_week":weeks-1,"date":Ddate},context_instance=RequestContext(request))
                data_aa={"username":user[0].chinese_name,'group':user[0].groupname,"task_info":task_info,
                        "ago_week":weeks+1,"week":weeks,"next_week":weeks-1,"date":Ddate}
                return render(request,'my_tasks.html',data_aa)
    uf=UserForm()
    return render(request,'login.html',{'uf':uf})

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
            return render(request,"manger.html",{"task_info":task_info,"username":user.chinese_name})
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
            return render(request,'task_list.html',{"users":users,"tasks":tasks,"username":username})
        except:pass
    return HttpResponseRedirect('/')

def show_per_all(request):
    if request.session:
        try:
            Uname=request.GET['user']
            user=User.objects.filter(chinese_name=Uname)[0]
            ID=request.session.get('user_id')
            cuser=User.objects.filter(id=ID)[0]
            try:
                weeks=int(request.GET['ago'])
            except:
                weeks=0
            week_c=int(time.strftime("%w"))
            tasks=[]
            today=datetime.date.today()
            s_Ddate=(today-datetime.timedelta(days=(week_c-1+7*weeks))).strftime('%Y-%m-%d')
            e_Ddate=(today-datetime.timedelta(days=(week_c-7+7*weeks))).strftime('%Y-%m-%d')
            Ddate=s_Ddate+" -- "+e_Ddate
            for i in range(1,8):
                _date=(today-datetime.timedelta(days=(week_c-i+7*weeks))).strftime('%Y%m%d')
                tasks.extend(task.objects.filter(user=user.chinese_name,IDD__contains=_date))
            task_info=sorted(tasks,key=lambda a:a.IDD,reverse=True)
            task_info=sorted(task_info,key=lambda a:a.status,reverse=True)
            data_aa={"user":user,"task_info":task_info,"cuser":cuser,"ago_week":weeks+1,"next_week":weeks-1,"date":Ddate,"type":1}
            return render(request,'task_per_all.html',data_aa)
        except Exception,e:
            print Exception,e
            pass
    return HttpResponseRedirect('/')

def show_per_all_month(request):
    if request.session:
        try:
            Uname=request.GET['user']
            user=User.objects.filter(chinese_name=Uname)[0]
            ID=request.session.get('user_id')
            cuser=User.objects.filter(id=ID)[0]
            try:
                months=int(request.GET['ago'])
            except:
                months=0
            tasks=[]
            today=datetime.date.today()
            year=today.year
            month=today.month-months
            while month<1:
                year-=1
                month+=12
            Ddate=datetime.datetime(year,month,1).strftime('%Y年%m月')
            DDdate=datetime.datetime(year,month,1).strftime('%Y%m')
            tasks.extend(task.objects.filter(user=user.chinese_name,IDD__contains=DDdate))
            task_info=sorted(tasks,key=lambda a:a.IDD,reverse=True)
            task_info=sorted(task_info,key=lambda a:a.status,reverse=True)
            return render(request,'task_per_all.html',{"user":user,"task_info":task_info,"cuser":cuser,"ago_week":months+1,"next_week":months-1,"date":Ddate,"type":2})
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
                return render(request,'xiafa_task.html',{"users":users,"cuser":user})
            elif request.method=="POST":
                now=datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d%H%M%S')
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
            return render(request,'person_info.html',{"user":user})
        elif request.method=="POST":
            user.chinese_name=request.POST["chinese_name"]
            user.photo_url=request.POST['photo_url']
            user.save()
            return render(request,'person_info.html',{"user":user,"TYPE":"1"})
        else:
            return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')

def weekly_tasks(request):
    if request.session:
        ID=request.session.get("user_id")
        if ID is None:return HttpResponseRedirect('/')
        user=User.objects.filter(id=ID)[0]
        if user.groupname=="admin":
            if request.method=="GET":
                weeks=int(request.GET['ago'])
                week_c=int(time.strftime("%w"))
                tasks=[]
                today=datetime.date.today()
                s_Ddate=(today-datetime.timedelta(days=(week_c-1+7*weeks))).strftime('%Y-%m-%d')
                e_Ddate=(today-datetime.timedelta(days=(week_c-7+7*weeks))).strftime('%Y-%m-%d')
                Ddate=s_Ddate+" -- "+e_Ddate
                for i in range(1,8):
                    _date=(today-datetime.timedelta(days=(week_c-i+7*weeks))).strftime('%Y%m%d')
                    tasks.extend(task.objects.filter(IDD__contains=_date))
                try:
                    if request.GET['download']=='true':
                        task_tables=[['IDD','日期'],['user','执行人'],['info','描述'],['Type','类型'],['status','进度'],['shenpi','审批'],['pingjia','评价']]
                        file_name="周报"+Ddate+'.xlsx'
                        return createdownloadfile(task_tables,tasks,file_name)
                except Exception,e:
                    print Exception,e
                return render(request,'weekly_tasks.html',{"user":user,"tasks":tasks,"ago_week":weeks+1,'week':weeks,"next_week":weeks-1,"date":Ddate})
        else:
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

def download(request):
    createdownloadfile()
    file_name='/tmp/task.xlsx'
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    response=StreamingHttpResponse(file_iterator(file_name),content_type='application/vnd.ms-excel')
    response['Content-Disposition']='attachment; filename="我的任务.xlsx"'
    return response
