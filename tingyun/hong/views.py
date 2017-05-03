# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hong.sphinxapi_core import *
import sys,time
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from hong.record import record as R
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
def detail_page(request):
	if request.GET.has_key('a'):
		#这里只有一条记录,直接查询即可
		data = request.GET['a']
		q = data.encode('utf-8')
		con2 = pymysql.connect(host='127.0.0.1', port=3306, user="root", passwd="liaohong", db="tingyun",charset="utf8")
		cursor = con2.cursor()
		sql_exec = "select * from copyright where id = {oid}".format(oid = q)
		cursor.execute(sql_exec)
		result = cursor.fetchall()
		return render(request,'detail_page.html',{'res':result})
		#return HttpResponse(res)
	elif request.POST.has_key('a'):	
		data = request.POST['a']
		q = data.encode('utf-8')
		con2 = pymysql.connect(host='127.0.0.1', port=3306, user="root", passwd="liaohong", db="tingyun",charset="utf8")
		cursor = con2.cursor()
		sql_exec = "select * from copyright where id = {oid}".format(oid = q)
		cursor.execute(sql_exec)
		result = cursor.fetchall()
		return render(request,'detail_page.html',{'res':result})
		#return HttpResponse(res)
	else:
		result = "没有和输入词相关的内容."
		return render(request,'error.html',{'res':result})

def final_page(request):
	if request.GET['oid']:
		res = request.GET['oid']
		#return render(request,'final_page.html',{'final_res':res})
		return HttpResponse(res)
	else:
		return HttpResponse("对不起没有东西返回")

def add(request):
	a = request.GET['user']
	#b = request.GET['b']
	#return HttpResponse(str(int(a)+int(b)))
	return HttpResponse(a)

def read_db_coreseek(request):
	if request.GET.has_key('search'):
		name = request.GET['search']
		q = name.encode('utf-8')
		R(q,request)
		#经过网页传输一次,所有的数据都成了unicode,需要转换成str才能正常使用
		mode = SPH_MATCH_ALL
		host = str('localhost')
		port = 9312
		index = str('*')
		filtercol = str('group_id')
		filtervals = []
		sortby = str('')
		groupby = str('')
		groupsort = str('@group desc')
		limit = 5
		
		# do query
		cl = SphinxClient()
		cl.SetServer ( host, port )
		cl.SetWeights ( [100, 1] )
		cl.SetMatchMode ( mode )
		if filtervals:
			cl.SetFilter ( filtercol, filtervals )
		if groupby:
			cl.SetGroupBy ( groupby, SPH_GROUPBY_ATTR, groupsort )
		if sortby:
			cl.SetSortMode ( SPH_SORT_EXTENDED, sortby )
		if limit:
			cl.SetLimits ( 0, limit, max(limit,1000) )
		res = cl.Query ( q, index )
		res_id = []
		map(lambda x:res_id.append(x['id']) , res['matches'])
		con2 = pymysql.connect(host='127.0.0.1', port=3306, user="root", passwd="liaohong", db="tingyun",charset="utf8")
		cursor = con2.cursor()
		sql_exec = "select * from copyright where id in {oid};"
		if len(res_id) > 1:
			res_id = tuple(res_id)
		elif len(res) == 1:
			res_id = "({name})".format(name=res[0]['id'])
		else:
			res_id = None
		if res_id:
			cursor.execute(sql_exec.format(oid=res_id))
			result = cursor.fetchall()
			cursor.close()
			return render(request,'read.html',{'res':result})
		else:
			result = "没有和输入词相关的内容."
			return render(request,'error.html',{'res':result})
	else:
		return HttpResponse("您要检索的关键词不存在")

	


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
#第一版本,基于sphinx自带的分词方法 ----  现已废弃,使用第二种coreseek
def read_index(request):
	if request.GET.has_key('search'):
		name = request.GET['search']
		#索引查询,拿取oid
		con1 = pymysql.connect(host='127.0.0.1', port=9306, user="root", passwd="liaohong", db="tingyun",charset="utf8")
		with con1.cursor(pymysql.cursors.DictCursor) as cur:
			cur.execute("select * from tingyun_index where match('{keyword}') limit 100".format(keyword = name))
			res = cur.fetchall()
		con2 = pymysql.connect(host='127.0.0.1', port=3306, user="root", passwd="liaohong", db="tingyun",charset="utf8")
		cursor = con2.cursor()
		sql_exec = "select * from copyright where id in {oid};"
		res_id = []
		if len(res) > 1:
			map(lambda x:res_id.append(x['id']) , res)
			res_id = tuple(res_id)
		elif len(res) == 1:
			res_id = "({name})".format(name=res[0]['id'])
		else:
			res_id = None
		if res_id:
			cursor.execute(sql_exec.format(oid=res_id))
			result = cursor.fetchall()
			return render(request,'read.html',{'res':result})
		else:
			result = "没有和输入词相关的内容."
			return render(request,'error.html',{'res':result})
	else:
		return HttpResponse("您要检索的关键词不存在")
		
		

	
	




