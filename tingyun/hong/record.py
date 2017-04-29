# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

def record(name,request):
	f = open('./hong/log.info','a+')
	if request.META.has_key('HTTP_X_FORWARDED_FOR'):
		print >> f,"at time %s , the ua is : %s , the access ip : %s:%s , keyword is : %s".encode('utf-8')%(time.ctime(),request.META.get('HTTP_USER_AGENT',None),request.META['HTTP_X_FORWARDED_FOR'],request.META.get('SERVER_PORT',None),name)
	else:
		print >> f,"at time %s , the ua is : %s , the access ip : %s:%s , keyword is : %s".encode('utf-8')%(time.ctime(),request.META.get('HTTP_USER_AGENT',None),request.META['REMOTE_ADDR'],request.META.get('SERVER_PORT',None),name)
	f.close()



