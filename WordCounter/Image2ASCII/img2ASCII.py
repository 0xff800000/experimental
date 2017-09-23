from PIL import Image

def img2char(str):
	img=Image.open(str)
	f=open('out.txt','w')
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			if img.getpixel((x,y))==(0,0,0):
				f.write('##')
			elif img.getpixel((x,y))==(0,0,0,255):
				f.write('##')
			else:
				f.write('  ')
		f.write('\n')
	f.close()
	img.close()
