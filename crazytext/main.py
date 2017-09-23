import random,sys

def screw(s,n):
	f=open('a.html','w')
	f.write('<p>')
	for c in s:
		f.write(c)
		for x in range(random.randint(1,n)):
			char=format(random.randint(768,879), '04x')
			f.write('&#x'+char+';')
	f.write('</p>')

screw(sys.argv[1],int(sys.argv[2]))