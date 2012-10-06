import urllib, urllib2, time
from grab import Grab, GrabError
from pyquery import PyQuery as pq
import re

def search_people():
	g = Grab()
	g.setup(post={'al': '1', 'c[age_from]': '21', 'c[name]': '1', 'c[section]': 'people', 'c[sex]': '1'})	
	try:
		g.go('http://vk.com/al_search.php')
		response = str(g.response.body)
		keys = []
		result = re.finditer('\d{8}', response)
		for match in result :
			if match.group() not in keys: #remove dublicates
				keys.append(match.group())
		return keys
	except Exception, detail: 
		return "Err ", detail 
