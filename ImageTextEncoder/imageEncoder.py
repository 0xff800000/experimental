from PIL import Image
import os
import string

def imgEncodByte(imgPath,textPath):
        img=Image.open(imgPath)
        if os.path.getsize(textPath)<img.size[1]*img.size[0]:
                f=open(textPath,'r')
                pixels = img.load()

                x=0;y=0
                txtLine=f.readline()
                while txtLine!='':
                        for character in range(len(txtLine)):
                                pixels[x,y]=(ord(txtLine[character]),pixels[x,y][1],pixels[x,y][1])
                                x+=1
                                if x==img.size[0]:x=0;y+=1
                                #for i in range(8):
                                        
                        txtLine=f.readline()
                f.close()
                img.save('mod.png')
                img.close()
        else:
                print('Text file too big.')

def imgDecodeByte(imgPath):
        img=Image.open(imgPath)
        f=open('decode.txt','w')
        pixels = img.load()

        for y in range(img.size[1]):
                for x in range(img.size[0]):
                        r,g,b=pixels[x,y]
                        char=''; char+=chr(r)
                        if char in string.printable:f.write(char)
        f.close()
        img.close()

def imgEncodBit(imgPath,textPath,channel):
        img=Image.open(imgPath)
        if os.path.getsize(textPath)*8/3<img.size[1]*img.size[0]:
                f=open(textPath,'r')
                pixels = img.load()

                x=0;y=0
                txtLine=f.readline()
                while txtLine!='':
                        for character in range(len(txtLine)):
                                for i in range(8):
                                        if channel=='r':
                                                pixels[x,y]=(0xff&(pixels[x,y][0]&~1)|(1&(ord(txtLine[character])>>i)),pixels[x,y][1],pixels[x,y][2])
                                        elif channel=='g':
                                                pixels[x,y]=(pixels[x,y][0],(pixels[x,y][1]&~1)|(1&(ord(txtLine[character])>>i)),pixels[x,y][2])
                                        elif channel=='b':
                                                pixels[x,y]=(pixels[x,y][0],pixels[x,y][1],(pixels[x,y][2]&~1)|(1&(ord(txtLine[character])>>i)))
                                        x+=1
                                        if x==img.size[0]:x=0;y+=1
                                        
                        txtLine=f.readline()
                f.close()
                img.save('mod.png')
                img.close()
        else:
                print('Text file too big.')

def imgDecodeBit(imgPath,channel):
        img=Image.open(imgPath)
        f=open('decode.txt','w')
        pixels = img.load()

        i=0;c=0
        for y in range(img.size[1]):
                for x in range(img.size[0]):
                        r,g,b=pixels[x,y]
                        if channel=='r': c|=(r&1)<<(i)
                        elif channel=='g': c|=(g&1)<<(i)
                        elif channel=='b': c|=(b&1)<<(i)
                        i+=1
                        if i==8:
                                i=0
                                char=chr(c)
                                c=0
                                if char in string.printable:f.write(char)
        f.close()
        img.close()
