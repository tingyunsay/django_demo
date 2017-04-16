#!coding:utf8

from django.http import HttpResponse

def home(request):
	return HttpResponse('hello, world')
