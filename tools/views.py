#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from web.models import User,information,Out
from django import forms
from django.template import RequestContext
import datetime
from dateutil import tz
import pytz,time
from django.http import StreamingHttpResponse
from Crypto.Cipher import Blowfish

def password_decrypte(request):
    try:
        if request.method=="GET":
            return render(request,'decrypte_passwd.html.template',{'passwd':""})
        elif request.method=="POST":
            password=request.POST['enctype_passwd']
            c1 = Blowfish.new('5F B0 45 A2 94 17 D9 16 C6 C6 A2 FF 06 41 82 B7'.replace(' ','').decode('hex'), Blowfish.MODE_CBC, '\x00'*8)
            c2 = Blowfish.new('24 A6 3D DE 5B D3 B3 82 9C 7E 06 F4 08 16 AA 07'.replace(' ','').decode('hex'), Blowfish.MODE_CBC, '\x00'*8)
            padded = c1.decrypt(c2.decrypt(password.decode('hex'))[4:-4])
            p = ''
            while padded[:2] != '\x00\x00' :
                p += padded[:2]
                padded = padded[2:]
            passwd=p.decode('UTF-16')
            return render(request,'decrypte_passwd.html.template',{"passwd":passwd})
    except:
        return render(request,'decrypte_passwd.html.template',{"passwd":"解密失败"})
