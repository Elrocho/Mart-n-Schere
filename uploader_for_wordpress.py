# encoding: utf-8

import vimeo, json, datetime, time
from time import gmtime, strftime
from HTMLParser import HTMLParser
from wordpress import API
import sys
import requests

# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

print "hello"

v = vimeo.VimeoClient(
token="#############",
key="##################",
secret="###################"
)
uploaded = set()
videos = set()
date = str(datetime.datetime.now())[:7]

base_url = "################"
api_path = "wp-json/wp/v2/"
wpapi = API(
url=base_url,
consumer_key="######",
consumer_secret="#############",
api="wp-json",
version="wp/v2",
wp_user="############",
wp_pass="#############",
oauth1a_3leg=True,
creds_store="~/.wc-api-creds.json",
callback="###########################"
)
resource = "posts?sort=date"
def wordpress_upload(string, title, categorie):
	data = {
		"content": string,
   		"title": title,
   		"status": "publish",
   		"categories": categorie,
   		"format" : "video",
   		"sticky" : True,
   		# You have way more options here! Example:
   		#"featured_media" : 
		}
	#try:
   	response = wpapi.post(base_url+api_path+resource, data)
   	#print(response.json())
	#except Exception as e:
   	#print("couldn't post")
	time.sleep(10)

def get_ids():
	response2 = wpapi.get(base_url+api_path+resource)
	for i5 in response2.json():
		if isinstance(i5, dict):
			for key5, value5 in i5.iteritems():
				if isinstance(value5, dict):
					for key6, value6 in i5["content"].iteritems():
						if isinstance(value6, unicode):
							try:
								__id = ((value6.split("external/")[1]).split(".hd")[0])
								uploaded.add(str(__id))
							except:
								pass
def check_id(theid):
	if theid in uploaded:
		print "already in!"
		return True
	else:
		return False
get_ids()
print uploaded
while True:
	try:
		my_videos = v.get("/me/videos?sort=date")
	except:
		my_videos = v.get("/me/videos?sort=date")

	dictionary = dict(my_videos.json())
	for key, value in dictionary.iteritems():
		if isinstance(value, list):
			for i in value:
				if isinstance(i, dict):
					if date in i[u'created_time']:
						theid = i[u"link"].split("/")[3]
						for i4 in i[u'files']:
							if i4[u'quality'] == "hd":
								videos.add(i4[u'link'].split('&')[0])
						for i9 in videos:
							if theid in i9:
								link_source = i9
						desc_dicti = i[u"description"]
						title_dicti = i[u"name"]
						print ("\n\n\n\n" + theid)
					###
						desc = desc_dicti if desc_dicti else ""
						categories = ["AGRO", "FERIAS", "REGIONALES"]
						#examples
						link = "<video width=\"800\" height=\"600\" controls=\"\"><source src=\"{l}\" type=\"video/mp4\"><source src=\"{l}\" type=\"video/ogg\"></video>".format(l=link_source)
						for cat in categories:
							if desc[:3] in cat:
								transform = {
									"AGRO" : 28,
									"FERIAS": 33,
									("GANADERÍA".decode("utf-8")) :30,
									("MAQUINARIA".decode("utf-8")): 32,
									"REGIONALES": 3
								}
								cate = transform[cat]
						try:
							but = ("<div class=\"wp-block-button\"><a class=\"wp-block-button__link has-text-color has-vlog-bg-color\" href=\"{}\">VER EN VIMEO</a></div>").format(i[u'link'])
						except:
							but = ("<div class=\"wp-block-button\"><a class=\"wp-block-button__link has-text-color has-vlog-bg-color\" href=\"{}\">VER EN VIMEO</a></div>").format(i[u'link'])

						if not check_id(theid):
							try:
								print "\n\n\n\n POST FOUND! \n\n POSTING...\n\n\n\n"
								string = link + "\n" + desc + "\n" + but
								wordpress_upload(string, title_dicti, cate)
								uploaded.add(theid)
							except NameError:
								print "sin boton"

					else:
						print "Nada por ahora... ult. actualizacion: " + str(strftime("%H:%M:%S", gmtime()))
						time.sleep(10)