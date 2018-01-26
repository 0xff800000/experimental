import urllib.request, random
from bs4 import BeautifulSoup

def get_tweets(username):
	url = urllib.request.urlopen( "https://twitter.com/" + username)
	page = BeautifulSoup( url ,"lxml")
	url.close()

	texts = []
	links = []
	for p in page.findAll("p"):
		if "class" in p.attrs:
			if 'tweet-text' in p.attrs["class"]:
				texts.append(p.text)

	return texts

print(random.choice(get_tweets("realDonaldTrump")))
