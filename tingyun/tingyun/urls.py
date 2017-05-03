"""tingyun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from . import views
from hong import views as hong_views
from django.conf.urls import * 
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$' , views.home),
    url(r'^home/' , hong_views.home),
    url(r'^hong/' , hong_views.late_hong),
    url(r'^add/' , hong_views.add),
    #url(r'^read/' , hong_views.read_db1),
    #url(r'^read/' , hong_views.read_index),
    url(r'^read/' , hong_views.read_db_coreseek),
    url(r'^final_page/' , hong_views.final_page),
    url(r'^detail_page/' , hong_views.detail_page),
]






