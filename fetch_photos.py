# -*- coding: utf-8 -*- 
import vk_auth
import search
import json
import urllib2
from urllib import urlencode
import json
import os
import os.path
import getpass
import sys
from pprint import pprint

numbers = 0;

def call_api(method, params, token):
    if isinstance(params, list):
        params_list = [kv for kv in params]
    elif isinstance(params, dict):
        params_list = params.items()
    else:
        params_list = [params]
    params_list.append(("access_token", token))
    url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params_list)) 
    return json.loads(urllib2.urlopen(url).read())["response"]

def get_albums(user_id, token):
    return call_api("photos.getAlbums", ("uid", user_id), token)

def get_photos_urls(user_id, album_id, token):
    photos_list = call_api("photos.get", [("uid", user_id), ("aid", album_id)], token)
    result = []
    for photo in photos_list:
        #Choose photo with largest resolution
        if "src_xxbig" in photo:
            url = photo["src_xxbig"]
        elif "src_xbig" in photo:
            url = photo["src_xbig"]
        else:
            url = photo["src_big"]
        result.append(url)
    return result

def save_photos(urls, album, directory):
    if not os.path.exists(str(directory)):
        os.mkdir(str(directory))
    names_pattern = "%%0%dd.jpg" % len(str(len(urls)))
    global numbers;
    for num, url in enumerate(urls):
        filename = os.path.join(str(directory), str(album) + '_' + names_pattern % (num + 1))
        print "Downloading %s" % filename
        open(filename, "w").write(urllib2.urlopen(url).read())
        numbers = numbers + 1
        if (numbers == 10) :
			return;

def save_on_disk(albums, user_id):
	choise = -1
	count = 0
	global numbers
	while choise not in xrange(len(albums)):
		count = count + 1
		photos_urls = get_photos_urls(user_id, albums[choise]["aid"], token)
		save_photos(photos_urls, count, user_id)
		if (numbers == 10) :
			return;
email = raw_input("Email: ")
password = getpass.getpass()
email = ''
password = ''
token, user_id = vk_auth.auth(email, password, "2951857", "photos")
user_id = 20020126

#res = search.search_people()

albums = get_albums(user_id, token)
save_on_disk(albums, user_id)
