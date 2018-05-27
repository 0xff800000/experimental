import urllib.request, random, time
from bs4 import BeautifulSoup

head = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0"}

languages = ["af","sq","am","ar","hy","az","eu","be","bn","bs","bg","ca","ceb ","zh-CN","zh-TW","co","hr","cs","da","nl","en","eo","et","fi","fr","fy","gl","ka","de","el","gu","ht","ha","haw ","iw","hi","hmn ","hu","is","ig","id","ga","it","ja","jw","kn","kk","km","ko","ku","ky","lo","la","lv","lt","lb","mk","mg","ms","ml","mt","mi","mr","mn","my","ne","no","ny","ps","fa","pl","pt","pa","ro","ru","sm","gd","sr","st","sn","sd","si","sk","sl","so","es","su","sw","sv","tl","tg","ta","te","th","tr","uk","ur","uz","vi","cy","xh","yi","yo","zu"]

def translate(hl,sl,txt):
	txt = urllib.parse.quote(txt)
	base_url = "https://translate.google.com/m?hl={}&sl={}&ie=UTF-8&prev=_m&q={}".format(hl,sl,txt)
	req = urllib.request.Request(base_url,headers=head)
	url = urllib.request.urlopen(req).read()
	page = BeautifulSoup( url ,"lxml")

	text = page.find_all(class_="t0")[0].text
	return text

def epicTranslate(txt,sl,n=10):
	print("--- Original text ---");
	print(txt)
	# Create translation path
	path = [random.choice(languages) for i in range(0,n)]
	path[0] = sl
	path[-1] = sl
	print("--- Path : {} ---".format(path))
	for i in range(0,n-1):
		print("--- Step {} : {}->{} ---".format(i,path[i],path[i+1]))
		txt = translate(path[i+1], path[i], txt)
		print(txt)
		time.sleep(2)
in_text = """Maître corbeau, sur un arbre perché,
        Tenait en son bec un fromage.
Maître renard par l'odeur alléché ,
        Lui tint à peu près ce langage :
        «Et bonjour Monsieur du Corbeau.
Que vous êtes joli! que vous me semblez beau!
        Sans mentir, si votre ramage
        Se rapporte à votre plumage,
Vous êtes le phénix des hôtes de ces bois»
A ces mots le corbeau ne se sent pas de joie;
        Et pour montrer sa belle voix,
Il ouvre un large bec laisse tomber sa proie.
Le renard s'en saisit et dit: "Mon bon Monsieur,
            Apprenez que tout flatteur
Vit aux dépens de celui qui l'écoute:
Cette leçon vaut bien un fromage sans doute."
        Le corbeau honteux et confus
Jura mais un peu tard , qu'on ne l'y prendrait plus."""
epicTranslate(in_text,"fr")
