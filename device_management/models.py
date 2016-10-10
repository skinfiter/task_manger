from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
# Create your models here.
class device_info(models.Model):
    create_date=models.CharField(max_length=24)
    brands=models.CharField(max_length=128)
    MODEL=models.CharField(max_length=128)
    serial_numbers=models.CharField(max_length=128)
    cpu=models.CharField(max_length=128)
    ram=models.CharField(max_length=128)
    storage=models.CharField(max_length=128)
    nic=models.CharField(max_length=128)
    count=models.IntegerField()
    attri=models.CharField(max_length=128)
    point=models.CharField(max_length=64)
    usage=models.CharField(max_length=256)
    info=models.TextField()
    create_user=models.CharField(max_length=64)

class device_info_Admin(admin.ModelAdmin):
    list_display=("id","create_date","brands","MODEL","serial_numbers","cpu","ram","storage","nic","count","attri","point","usage","info","create_user")

admin.site.register(device_info,device_info_Admin)
