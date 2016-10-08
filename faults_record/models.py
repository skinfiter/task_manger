from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.


class fault_info(models.Model):
    create_time=models.CharField(max_length=50)
    point=models.CharField(max_length=50)
    product=models.CharField(max_length=200)
    fault_device=models.CharField(max_length=50)
    fault_type=models.CharField(max_length=32)
    info=models.TextField()
    method=models.TextField()
    deal_chinese_name=models.CharField(max_length=32)

class fault_infoAdmin(admin.ModelAdmin):
    list_display=("create_time","point","product","fault_device","fault_type","info","method","deal_chinese_name")

class point(models.Model):
    point_name=models.CharField(max_length=64)

class pointAdmin(admin.ModelAdmin):
    list_display=("id","point_name")

class product(models.Model):
    name=models.CharField(max_length=64)

class productAdmin(admin.ModelAdmin):
    list_display=("id","name")

admin.site.register(fault_info,fault_infoAdmin)
admin.site.register(point,pointAdmin)
admin.site.register(product,productAdmin)
