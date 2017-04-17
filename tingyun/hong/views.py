# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from hong.models import Copyright
def home(request):
	return render(request,'home.html')

def late_hong(request):
	#if request.GET.has_key('user'):
	#	name = '-'+request.GET['user']
	res = Copyright.objects.order_by('id')
	
	return render(request,'hong.html',{'res':res[:10]})
		#return HttpResponse(res)
	#else:
		#return HttpResponse("这次我没连接数据库")
		#res = Copyright.objects.order_by('-artist_info')
	#return render(request,'hong.html')
def add(request):
	a = request.GET['user']
	#b = request.GET['b']
	#return HttpResponse(str(int(a)+int(b)))
	return HttpResponse(a)

#读取数据函数
def read_db1(request):
	if request.GET.has_key('user'):
	#	print "11111111111"
		name = request.GET['user']
	#	print name
		res = Copyright.objects.order_by(name)
		#这个return是讲数据填充到了模板中,然后再返回的....我真是...
		return render(request,'read.html',{'res':res[:2]})
	#return HttpResponse(res)
	else:
		return HttpResponse("请检查输入是否有错误.")


