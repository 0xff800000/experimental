from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

print('Start')

device = MonkeyRunner.waitForConnection()

coords=[(97,522),(234,522),(384,522),(523,522)]

def scanCoord():
	notes=[]
	newimage=device.takeSnapshot()
	for c in coords:
		a,r,g,b=newimage.getRawPixel(c[0],c[1])
		if (r,g,b)!=(255,255,255):
			notes.append(c)
		print((a,r,g,b))
	return notes

def tapCoord(coord):
	for c in coord:
		device.touch(int(c[0]),int(c[1]),'DOWN_AND_UP')


while True:
	tapCoord(scanCoord())
	#device.sleep(0.5)