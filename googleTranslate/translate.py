import urllib.request, random
from bs4 import BeautifulSoup

head = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0"}

def translate(hl,sl,txt):
	txt = urllib.parse.quote(txt)
	base_url = "https://translate.google.com/m?hl={}&sl={}&ie=UTF-8&prev=_m&q={}".format(hl,sl,txt)
	req = urllib.request.Request(base_url,headers=head)
	url = urllib.request.urlopen(req).read()
	page = BeautifulSoup( url ,"lxml")

	text = page.find_all(class_="t0")[0].text
	return text

print(translate("fr","en","I'm hungry."))
