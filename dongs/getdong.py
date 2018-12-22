import json
import urllib.request
from bs4 import BeautifulSoup
url = "http://dongs2.blogspot.com/p/all-dongs-no-pictures-nor-description.html"
def getdong(url):
	r = urllib.request.urlopen(url)
	soup = BeautifulSoup(r,'html.parser')
	return soup
def getli(url):
	olist=list()
	soup = getdong(url)
	for ol in soup.find_all('ol'):
		for li in ol.find_all('li'):
			for a in li.find_all('a',href=True):
				olist.append(a['href'].encode('utf-8'))
	return olist
def dumperstriper(url):
	alist = getli(url)
	strlist = []
	for link in alist:
		link = str(link)
		link = link[1:]
		strlist.append(link)
	with open('dongs.txt','w') as file:
		json.dump(strlist, file)
dumperstriper(url)