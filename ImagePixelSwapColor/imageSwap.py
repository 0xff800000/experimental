from PIL import Image
import os, sys, random

def get_rand_color():
	return (random.randint(0,256),random.randint(0,256),random.randint(0,256))

def imgSwap(imgPath):
	img=Image.open(imgPath)
	pixels = img.load()
	
	pixel_dict = {}
	used_colors = []

	for y in range(img.size[1]):
		for x in range(img.size[0]):
			if pixels[x,y] in pixel_dict:
				pixels[x,y] = pixel_dict[pixels[x,y]]
			else:
				new_color = get_rand_color()
				while new_color in used_colors:
					new_color = get_rand_color()
				pixel_dict[pixels[x,y]] = new_color
				pixels[x,y] = new_color
				new_color = get_rand_color()
				used_colors.append(new_color)

	path = '.'.join(imgPath.split(".")[0:-2])
	name = imgPath.split(".")[-2]
	ext = imgPath.split(".")[-1]
	img.save(path+name+'SWAP.'+ext)
	img.close()

imgSwap(sys.argv[1])
