#!/usr/bin/python
#!coding:utf8
from urllib import unquote,quote
import requests
import re
from bs4 import BeautifulSoup
from tqdm import *
import time

#备选词库,关键词相关
#key_word = ["明星","歌手"]
key_word = ["歌手"]

#传入关键词库,返回一级页面
def get_first(key_word):
	first_urls = []
	map(lambda i:first_urls.append("http://pinyin.sogou.com/dict/search/search_list/{key}/normal/1".format(key=quote(i.decode('utf-8').encode('gbk')))) , key_word)
	return first_urls

#先按照原先字符编码 解码成为 unicode, 之后再编码成 想要的编码 , 最后再使用quote替换成 网页编码
#print quote(key_word[0].decode('utf-8').encode('gbk'))

def get_second(first_urls):
	second_urls = []
	for url in first_urls:
		res = requests.get(url).content
		soup = BeautifulSoup(res,"lxml")
		page_num = (soup.select('#dict_page_list > ul > li > span > a')[-2]).text
		for i in range(1,int(page_num)+1):
			second_urls.append(re.sub('\d+$',str(i),url))
	return second_urls

def get_third(second_urls):
	dicts = []
	for url in second_urls:
		soup = BeautifulSoup(requests.get(url).content,"lxml")
		temp = soup.select('.dict_dl_btn > a')
		map(lambda i:dicts.append(i.attrs['href'].encode('unicode_escape').decode('gbk').encode('utf-8')) , temp)
	return dicts


def download(url):
	with open('./sougou/{name}.scel'.format(name=j),'wb') as f:
		f.write(requests.get(url).content)
	f.close()

if __name__ == '__main__':
	first_urls = get_first(key_word)
	second_urls = get_second(first_urls)
	third_urls = get_third(second_urls)
	print "开始下载......"
	j = 0
	counts = len(third_urls)

	#tqdm装饰在任意一个迭代器上,能显示当前迭代的进度
	for url in tqdm(third_urls):
		time.sleep(0.01)
		download(url)
		j += 1
		#print "下载{name}.scel完成,当前进度为{status} %".format(name = j,status = str(float(j)/counts *100))
	print "下载完毕,开始导入词典......"
	
	
	

