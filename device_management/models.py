from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
# Create your models here.
class device_info(models.Model):
    create_user=models.IntegerField()
    brands=models.CharField(max_length=128)
    MODEL=models.CharField(max_length=128)
    serial_numbers=models.CharField(max_length=128)
    count=models.IntegerField()
    attri=models.CharField(max_length=128)
    info=models.TextField()
    usage=models.CharField(max_length=256)

class device_info_Admin(admin.ModelAdmin):
    list_display=("create_user","brands","MODEL","serial_numbers","count","attri","info","usage")

admin.site.register(device_info,device_info_Admin)
