from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
# Create your models here.

class User(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=50)
    groupname=models.CharField(max_length=200)
    chinese_name=models.CharField(max_length=32)
    photo_url=models.CharField(max_length=256)


class Group(models.Model):
    groupName=models.CharField(max_length=200)

class GroupAdmin(admin.ModelAdmin):
    list_display=("groupName",)

class UserAdmin(admin.ModelAdmin):
    list_display=('username','password',"groupname","chinese_name")
    search_fields=("groupname",)

class Out(models.Model):
    out_name=models.CharField(max_length=200)
    out_chinese_name=models.CharField(max_length=200)
    group=models.CharField(max_length=200)

class OutAdmin(admin.ModelAdmin):
    list_display=('out_name','out_chinese_name','group')

class information(models.Model):
    user=models.CharField(max_length=200)
    date=models.CharField(max_length=200)
    out_name=models.CharField(max_length=200)
    out=models.CharField(max_length=200)
    status=models.CharField(max_length=10)

class task(models.Model):
    IDD=models.CharField(max_length=32)
    info=models.TextField()
    Type=models.CharField(max_length=16)
    status=models.CharField(max_length=16)
    shenpi=models.CharField(max_length=16)
    user=models.CharField(max_length=32)
    pingjia=models.CharField(max_length=4)
    createUserGroup=models.CharField(max_length=32)

class TaskAdmin(admin.ModelAdmin):
    list_display=('IDD','info','Type','status','shenpi','user','pingjia')

admin.site.register(User,UserAdmin)
admin.site.register(information)
admin.site.register(Group,GroupAdmin)
admin.site.register(Out,OutAdmin)
admin.site.register(task,TaskAdmin)
