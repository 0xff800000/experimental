import struct,os,sys,math
bytesPerPix = 3
img=open(sys.argv[1],'r').read()
width = math.sqrt(len(img))
height = math.sqrt(len(img))
f=open("test.bmp",'wb')
f.write("BM")
f.write(struct.pack("<i",width*height*bytesPerPix)) #file size
f.write(bytearray(4)) #file
f.write(struct.pack("<i",54)) #pixels offset
f.write(struct.pack("<i",40)) #Header size
f.write(struct.pack("<i",width)) #width
f.write(struct.pack("<i",height)) #height
f.write(struct.pack("<h",1)) # 1
f.write(struct.pack("<h",8*bytesPerPix)) #bit per pixel
f.write(struct.pack("<i",0)) #compression
f.write(struct.pack("<i",0)) #image size
f.write('\x00'*4) #prefer resol x pix/m
f.write('\x00'*4) #prefer resol y pix/m
f.write('\x00'*4) #color used
f.write('\x00'*4) #color significant

f.write(img)
# for x in range(width):
#     for y in range(height):
#         r=(x/width)*0xff
#         g=(y/height)*0xff
#         f.write(chr(255))
#         f.write(chr(g))
#         f.write(chr(0))
#f.write("\x00\xff\xff")

#f.write("\xff\x00\x00"*((width*height)))
