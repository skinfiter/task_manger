"""home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web import views
from web import my_task
#import captcha

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.login),
    url(r'^post',views.post_flow),
    url(r'^data.json$',views.get_json),
#    url(r'^captcha/',captcha.urls),
    url(r'^add_task',views.add_task),
    url(r'^task/complate',views.complate_task),
    url(r'^task/del',views.del_task),
    url(r'^shenpi$',my_task.shenpi),
    url(r'^logout$',my_task.logout),
    url(r'^task/pass',my_task.bypass),
    url(r'^task_per$',my_task.task_per),
    url(r'^show$',my_task.show_per_all),
    url(r'^xiafa_task$',my_task.xiafa_task),
    url(r'^person$',my_task.person),
]
