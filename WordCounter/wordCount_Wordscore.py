import re

def printf(s):
        s=str(s)
        print(s)

blacklist = []

def getBlackList():
        f = open('blacklist.txt','r', encoding="utf8")
        line = f.readline()
        while line != '':
                word = line.lower()
                word = word.split('\n')[0]
                blacklist.append(word)
                line = f.readline()

separator = "\(|\)|\[|\]|>|<|,|<|\.|!|/| |\|:|\'|\"|\n|\t|•|“|«|»|’|”|_|-"

def getWordScore(path):
        f=open(path,'r', encoding="utf8")
        wordsCount = {}
        # Counting words
        line = f.readline()
        while line != '':
                #print(line)
                words=line.lower()
                words=re.split(separator,words)
                for w in words:
                        if len(w)<=1: continue
                        if w in blacklist: continue
                        if w in wordsCount:
                                wordsCount[w]+=1
                        else:
                                wordsCount[w]=1
                line = f.readline()
        f.close()

        # Sorting
        stat=[]
        for w in wordsCount:
                stat.append((wordsCount[w],w))
        stat.sort(reverse=True)
        return stat

def getSentence(path):
        f=open(path,'r', encoding="utf8")
        text = ''
        # Get all text
        line = f.readline()
        while line != '':
                text += line
                line = f.readline()
        f.close()
        text = re.split("\.|!|\?|;|\|",text)
        # Get score words
        wordScore = getWordScore('in.txt')
        ws = {}
        for i,w in enumerate(wordScore):
                #ws[w[1]]=len(wordScore)-i
                ws[w[1]]=len(wordScore)-i
        sentenceScore = []
        for s in text:
                s=s.replace('\n',' ')
                score=0
                ss = re.split(separator,s)
                if len(ss) < 1: continue
                for w in ss:
                        if w in ws:
                                score += ws[w]
                #score = score / len(ss)
                sentenceScore.append((score,s))
        sentenceScore.sort(reverse=True)
        return sentenceScore



## Main
getBlackList()
wc = getWordScore('in.txt')
wc=getSentence('in.txt')
# Printing words
f=open('out.txt','w', encoding="utf8")
for count,word in wc:
        #print(w)
        f.write('{} \nSCORE : {}\n\n\n'.format(word,count))
