#coding=utf-8
from web.models import User,information,Out,task

def get_outs(group_name):
    a={}
    if group_name=="admin":
        outs=Out.objects.all()
    else:
        outs=Out.objects.filter(group=group_name)
    for out in outs:
        a[out.out_name]=out.out_chinese_name
    return a

def get_tasks(user1="admin"):
    a=[]
    if user1=="admin":
        tasks=task.objects.all()
    else:
        tasks=task.objects.filter(user=user1)
    for task1 in tasks:
        a.append({'IDD':task1.IDD,'info':task1.info,'type':task1.Type,'status':task1.status,'shenpi':task1.shenpi,'user':task1.user})
    return a
