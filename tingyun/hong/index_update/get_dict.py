#!/usr/bin/python
#!coding:utf8
# @author: tingyun
# @date: 2017-04-29
# @depends: python2.7.+
from urllib import unquote,quote
import requests
import re,os,sys
import commands
from bs4 import BeautifulSoup
from tqdm import *
import time

#备选词库,关键词相关,可手动添加
key_word = ["明星","歌手"]
#key_word = ["歌手"]

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
	print "下载完毕,开始导入词典.....\n"
	commands.getoutput("./extract-sougou-dict.py sougou/*.scel -o sougou-dict.txt -mmseg")
	
	print "\t1. 生成词库成功,合并新词典....."
	if not os.path.exists("/usr/local/mmseg3/etc/unigram.txt"):
		print "\t请检查文件 /usr/local/mmseg3/etc/unigram.txt 是否存在!"
		sys.exit()
	os.system("cp /usr/local/mmseg3/etc/unigram.txt ./")
	commands.getoutput("./merge-mmseg-dict.py -a unigram.txt -b sougou-dict.txt -o merged.txt")
	
	print "\t2. 合并词典成功,备份旧版本到 /usr/local/mmseg3/bak/ 下,并更新...."
	if not os.path.exists("/usr/local/mmseg3/bak"):
		os.mkdir("/usr/local/mmseg3/bak")
	#我们只需要保存上一版本的,如果新版本的词典出错,那么直接使用上一版本,重新建立索引.
	#所以这个脚本不应该是每天都会运行,应该是一定时间跑一次,因为涉及到重建索引,时间很长
	commands.getoutput("mv /usr/local/mmseg3/etc/unigram.txt /usr/local/mmseg3/bak/unigram.txt.bak")
	if not os.path.exists("/usr/local/mmseg3/etc/uni.lib"):
		print "\t请检查文件 /usr/local/mmseg3/etc/uni.lib 是否存在!"
		sys.exit()
	commands.getoutput("mv /usr/local/mmseg3/etc/uni.lib /usr/local/mmseg3/bak/uni.lib.bak")
	print "\t\t备份完成,保存至 /usr/local/mmseg3/bak/"

	commands.getoutput("mv ./merged.txt /usr/local/mmseg3/etc/unigram.txt")
	commands.getoutput("/usr/local/mmseg3/bin/mmseg -u /usr/local/mmseg3/etc/unigram.txt")

	if not os.path.exists("/usr/local/mmseg3/etc/unigram.txt.uni"):
		print "未正确生成 .lib 文件,请检查unigram.txt文件是否正确."
		sys.exit()
	commands.getoutput("cd /usr/local/mmseg3/etc && mv unigram.txt.uni uni.lib")
	if os.path.exists("/usr/local/mmseg3/etc/uni.lib"):
		print "\t3.词典更新完成."
	else:
		print "\t3.词典未正确更新,请检查错误."
		sys.exit()
	print "all done."
	
	
	
	
	
