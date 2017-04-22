# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from hong.models import Copyright
import pymysql
import pandas


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
		name = request.GET['user']
		res = Copyright.objects.order_by(name)
		#这个return是将数据填充到了模板中,然后再返回的....我真是...
		return render(request,'read.html',{'res':res[:2]})
	else:
		return HttpResponse("请检查输入是否有错误.")

#读取传入的参数,使用索引检索相关项目,最后返回是mysql中的数据
def read_index(request):
	if request.GET.has_key('search'):
		name = request.GET['search']
		print name,":type = ",type(name)
		#索引查询,拿取oid
		con1 = pymysql.connect(host='127.0.0.1', port=9306, user="root", passwd="liaohong", db="tingyun",charset="utf8")
		with con1.cursor(pymysql.cursors.DictCursor) as cur:
			cur.execute("select * from tingyun_index where match('{keyword}') limit 100".format(keyword = name))
			res = cur.fetchall()
		con2 = pymysql.connect(host='127.0.0.1', port=3306, user="root", passwd="liaohong", db="tingyun",charset="utf8")
		cursor = con2.cursor()
		sql_exec = "select * from copyright where id in {oid};"
		res_id = []
		map(lambda x:res_id.append(x['id']) , res)
		if res_id:
			cursor.execute(sql_exec.format(oid=tuple(res_id)))
			result = cursor.fetchall()
			return render(request,'read.html',{'res':result})
		else:
			result = "没有和输入词相关的内容."
			return render(request,'error.html',{'res':result})
	else:
		return HttpResponse("您要检索的关键词不存在")
		
		

	
	




