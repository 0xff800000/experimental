from PIL import Image
import os, sys, random

def get_rand_color():
	return (random.randint(0,256),random.randint(0,256),random.randint(0,256))

def imgSwap(imgPath):
	img=Image.open(imgPath)
	pixels = img.load()
	
	offset = random.randint(0,256000)

	for y in range(img.size[1]):
		for x in range(img.size[0]):
			r,g,b = pixels[x,y]
			pixels[x,y] = ((r+offset)%256,(g+offset)%256,(b+offset)%256)
			
	path = '.'.join(imgPath.split(".")[0:-2])
	name = imgPath.split(".")[-2]
	ext = imgPath.split(".")[-1]
	img.save(path+name+'SWEEP.'+ext)
	img.close()

imgSwap(sys.argv[1])
