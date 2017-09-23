import re

f=open('in.txt','r', encoding="utf8")

wordsCount = {}
separator = "\(|\)|\[|\]|>|<|,|<|\.|!|/| |\|:|\'|\"|\n|\t|•|“|«|»|’|”|_|-"

# Counting words
line = f.readline()
while line != '':
        #print(line)
        words=line.lower()
        words=re.split(separator,words)
        for w in words:
                if len(w)<=1: continue
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

# Printing words
f=open('out.txt','w', encoding="utf8")
for num,w in stat:
        #print(w)
        f.write('{} : {}\n'.format(w,wordsCount[w]))
