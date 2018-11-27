from PIL import Image
import os
import string
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread,imsave

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
        img.show()
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


def imageRot(imgPath):
        pixels = imread(imgPath)
        orig_size = pixels.shape
        new_size = (orig_size[0]-30,-1,3)
        print(new_size)
        img = np.reshape(pixels,(1,-1))
        img = np.roll(img,100)
        #img = np.roll(img,100,axis=1)
        img = np.reshape(img,new_size)
        plt.imshow(img)
        plt.show()

imageRot('a.png')
