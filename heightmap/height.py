import sys
from PIL import Image

def img2obj(filepath):
	spacing = 0.10
	img=Image.open(filepath)
	vertex = []

	# Open and write the header of the obj file
	f=open('{}.obj'.format(filepath),'w')
	f.write('o {}\n'.format(filepath))

	# Parse the image and extract verticies
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			pix = img.getpixel((x,y))
			z = (pix[0] + pix[1] + pix[2]) / (3.0*255.0)
			v = (spacing*x, spacing*y, spacing*z)
			vertex.append(v)

			# Write vertex to file
			f.write('v {} {} {}\n'.format(v[0],v[2],v[1]))
	f.write('\nusemtl None\ns off\n')

	# Reconstruct the faces
	w = img.size[0]
	h = img.size[1]-1
	faceCnt = 1
	for y in range(h):
		f.write('# Line {}\n'.format(y+1))
		for x in range(w):
			if x+1 == w:
				break
			current = (x+1) + (y) * w
			face = [current, current + w + 0, current + w + 1, current + 1]
			s = 'f'
			for fa in face:
				s += ' ' + str(fa) + '//' + str(faceCnt)
			s += '\n'
			faceCnt += 1
			# Write face to file
			f.write(s)
	# w = img.size[0]-1
	# h = img.size[1]-1
	# faceCnt = 1
	# for x in range(w*h):
	# 	current = x+1
	# 	face = [current, current + 1, current + w + 2, current + w + 1]
	# 	s = 'f'
	# 	for fa in face:
	# 		s += ' ' + str(fa) + '//' + str(faceCnt)
	# 	s += '\n'
	# 	faceCnt += 1
	# 	# Write face to file
	# 	f.write(s)
	f.close()
	img.close()

img2obj(sys.argv[1])
