from PIL import Image
color0='░░'
color1='▒▒'
color2='▓▓'
color3='██'
endl=b'\n'
def img2char(str):
        img=Image.open(str)
        pixels=img.load()
        f=open('out.txt','wb')
        for y in range(img.size[1]):
                for x in range(img.size[0]):
                        avg=(pixels[x,y][0]+pixels[x,y][1]+pixels[x,y][2])/3
                        if avg<64:
                                f.write(color3.encode('utf8'))
                        elif avg<128:
                                f.write(color2.encode('utf8'))
                        elif avg<192:
                                f.write(color1.encode('utf8'))
                        elif avg>192:
                                f.write(color0.encode('utf8'))
                #f.write(endl.encode('utf8'))
                f.write(endl)
        f.close()
        img.close()
