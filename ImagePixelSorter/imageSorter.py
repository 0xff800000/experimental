from PIL import Image
import os
import string

def imgSort(imgPath):
        img=Image.open(imgPath)
        
        pixels = img.load()

        for y in range(img.size[1]):
                pixelLine=[]
                for x in range(img.size[0]):
                        pixelLine.append(pixels[x,y])

                pixelLine.sort()
                
                for x in range(img.size[0]):
                        pixels[x,y]=pixelLine[x]
        img.save('mod.png')
        img.close()

def blackAndWhite(imgPath):
        img=Image.open(imgPath)
        
        pixels = img.load()

        for y in range(img.size[1]):
                for x in range(img.size[0]):
                        avg=int((pixels[x,y][0]+pixels[x,y][1]+pixels[x,y][2])/3)
                        pixels[x,y]=(avg,avg,avg)
        img.save('mod.png')
        img.close()
