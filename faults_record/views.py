#encoding=utf-8
from django.shortcuts import render,render_to_response
from web.models import User
from faults_record.models import fault_info,point,product
import pytz,time,datetime
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.

def show_faults(request):
    try:
        ID=request.session.get('user_id')
        user=User.objects.filter(id=ID)
        try:
            weeks=int(request.GET['ago'])
        except Exception,e:
            weeks=0
        week_c=int(time.strftime("%w"))
        fault_infos=[]
        today=datetime.date.today()
        year=today.year
        month=today.month-weeks
        while month<1:
            year-=1
            month+=12
        Ddate=datetime.datetime(year,month,1).strftime('%Y年%m月')
        DDdate=datetime.datetime(year,month,1).strftime('%Y-%m')
        fault_infos=fault_info.objects.filter(create_time__contains=DDdate)
#        task_info=sorted(tasks,key=lambda a:a.IDD,reverse=True)
#        task_info=sorted(task_info,key=lambda a:a.status,reverse=True)
        return render_to_response('show_faults.html',{"fault_infos":fault_infos,"ago_week":weeks+1,"next_week":weeks-1,"date":Ddate},context_instance=RequestContext(request))
    except Exception,e:
        return HttpResponseRedirect('/')

def add_fault(request):
    if request.method=='POST':
        ID=request.session.get('user_id')
        try:
            user=User.objects.filter(id=ID)[0]
        except Exception,e:
            return HttpResponseRedirect('/')
        _point=point.objects.filter(id=request.POST['point'])[0]
        _product=product.objects.filter(id=request.POST['product'])[0]
        fault_device_ip=request.POST['fault_device_ip']
        fault_type=request.POST['fault_type']
        info=request.POST['fault_info']
        method=request.POST['method']
        try:
            now=datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
            fault_info.objects.create(create_time=now,deal_chinese_name=user.chinese_name,point=_point.point_name,product=_product.name,fault_device=fault_device_ip,fault_type=fault_type,info=info,method=method)
            return HttpResponseRedirect('/show_faults')
        except Exception,e:
            print Exception,e
            return render_to_response('faild.html',{"title":"添加故障信息失败，返回任务记录界面"},context_instance=RequestContext(request))
    else:
        if request.session:
            ID=request.session.get('user_id')
            user=User.objects.filter(id=ID)
            if len(user)<1:return HttpResponseRedirect('/')
            points=point.objects.all()
            products=product.objects.all()
            return render_to_response("add_fault.html",{"username":user[0].chinese_name,"points":points,"products":products},context_instance=RequestContext(request))
        else:
            uf=UserForm()
            return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))
