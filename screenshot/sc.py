import struct,os
width = 1600
height = 900
os.system("cat /dev/fb0 > o.o")
img =open('o.o','rb').read()
os.system("rm o.o")
f=open("test.bmp",'wb')
f.write("BM")
f.write(struct.pack("<i",width*height*4)) #file size
f.write(bytearray(4)) #file
f.write(struct.pack("<i",54)) #pixels offset
f.write(struct.pack("<i",40)) #Header size
f.write(struct.pack("<i",width)) #width
f.write(struct.pack("<i",height)) #height
f.write(struct.pack("<h",1)) # 1
f.write(struct.pack("<h",32)) #bit per pixel
f.write(struct.pack("<i",0)) #compression
f.write(struct.pack("<i",0)) #image size
f.write('\x00'*4) #prefer resol x pix/m
f.write('\x00'*4) #prefer resol y pix/m
f.write('\x00'*4) #color used
f.write('\x00'*4) #color significant
#f.write(bytearray(7)) #file
f.write(img)
#f.write("\x00\xff\xff")
#f.write("\xff\x00\x00"*((width*height)))
