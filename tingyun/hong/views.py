# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hong.sphinxapi_core import *
import sys,time
from django.shortcuts import render
import json
from django.http import HttpResponse
# Create your views here.
from hong.record import record as R
from hong.models import Copyright
import pymysql
import pandas
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
	return render(request,'home.html')

def test(request):

	#beatles_list = Copyright.objects.all()
	beatles_list =(1,2,3,4,5,6,7,8,9,10,11,12)
	# 分页器，对 beatles_list 进行分页操作，每页显示2个对象
	paginator = Paginator(list(beatles_list), 5) 
	# get 方法获取页数
	page = request.GET.get('page')
	
	try: # 获取某页
		beatles_list = paginator.page(page)
	except PageNotAnInteger: # 如果 page 参数不为正整数，显示第一页
		beatles_list = paginator.page(1)
	except EmptyPage: # 如果 page 参数为空页，跳到最后一页
		beatles_list = paginator.page(paginator.num_pages)

	#context['beatles_list'] = beatles_list

	return render(request, 'test.html', {"res":beatles_list})

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
		content = {}
		data = request.POST['a']
		q = data.encode('utf-8')
		name = request.POST.get('b')
		con2 = pymysql.connect(host='127.0.0.1', port=3306, user="root", passwd="liaohong", db="tingyun",charset="utf8")
		cursor = con2.cursor()
		sql_exec = "select * from copyright where id = {oid}".format(oid = q)
		cursor.execute(sql_exec)
		result = cursor.fetchall()
		content['a'] = result
		content['b'] = name
		return render(request,'detail_page.html',{'res':content})
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

def read_db_coreseek(request):
	if request.GET.get('search'):
		name = request.GET.get('search')
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
		limit = 20
	
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
		#if res_id:
		cursor.execute(sql_exec.format(oid=res_id))
		result = cursor.fetchall()
		cursor.close()
		
		#添加分页代码
		content = {}
		contacts = list(result)
		'''
		paginator = Paginator(contacts, 3)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
			contacts = paginator.page(1)
		except EmptyPage:
			contacts = paginator.page(paginator.num_pages)
		'''
		content['a'] = contacts
		content['b'] = q
		#return HttpResponse(contacts)
		return render(request,'read.html',{"res":content})
		#return render(request,'read.html',{"res":json.dumps(contacts)})
	else:
		result = "请输入关键词,否则无法检索."
		return render(request,'error.html',{'res':result})
def cut_page(request):
	result = request.GET.get('info')
	paginator = Paginator(result, 5)
	print  paginator
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)
	return render(request,'read.html',{'page':contacts})


def add(request):
	a = request.GET['user']
	#b = request.GET['b']
	#return HttpResponse(str(int(a)+int(b)))
	return HttpResponse(a)
'''
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
'''
	


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
		
		

	
	




