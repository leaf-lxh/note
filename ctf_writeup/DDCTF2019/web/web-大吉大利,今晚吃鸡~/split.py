#!/usr/bin/python3
#coding: utf8
"""
读取result.txt，提交id和ticket
"""

import urllib.request
import time
reflection = {}
with open("result.txt", 'r') as result:
	lines = result.readlines()
	for i in lines:
		reflection[i[:i.find(' | ')]] = i[i.find(' | ')+3:]

result = []
for k in reflection.keys():
	url = "http://117.51.147.155:5050/ctf/api/remove_robot?id=%s&ticket=%s" % (k, reflection[k])
	url = urllib.request.Request(url, headers={"cookie":"user_name=leaflxh; REVEL_SESSION=a834d13f1a5e6254e4030fc42ad2917b"})
	urllib.request.urlopen(url)
	print(k)
	# try:
	#查找1到149中哪个ID没跑出来
	# 	result.append(int(k))
	# except ValueError:
	# 	continue
#exit(0)	
# result.sort()
# print(result)
# print(reflection['52'])
# for i in range(1,150):
# 	if i not in result:
# 		print(i, "not in the list")
