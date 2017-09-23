from PIL import Image

def img2array(str):
        # Open image
        img = Image.open(str)
        pixels = img.load()
        # Create output file
        fileName = str.split('.')[0]
        f = open(fileName+'.h','w')
        # Write begin header
        f.write('#ifndef {}_H\n#define {}_H\n\n'.format(fileName.upper(),fileName.upper()))
        # Declarations
        f.write('const int {}Width = {};\n'.format(fileName,img.size[0]))
        f.write('const int {}Height = {};\n\n'.format(fileName,img.size[1]))
        f.write('const char {}[] = {{'.format(fileName))
        for y in range(img.size[1]):
                for x in range(img.size[0]):
                        r,g,b = pixels[x,y]
                        if y==img.size[1]-1 and x==img.size[0]-1:
                                f.write(' {}, {}, {} }};\n\n'.format(hex(r),hex(g),hex(b)))
                        else:
                                f.write(' {}, {}, {},'.format(hex(r),hex(g),hex(b)))
        f.write('#endif\n')
        f.close()
        img.close()

img2array('gandalf.jpg')
