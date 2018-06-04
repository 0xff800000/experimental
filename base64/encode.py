import base64, sys

def encodeFile(path):
	fr = open(path,'rb')
	data = fr.read()
	dataEncoded = base64.b64encode(data)
	fw = open(path+'.txt', 'wb')
	fw.write(dataEncoded)
	fr.close()
	fw.close()

def decodeFile(path):
	new_path = path.split(".txt")[0]
	fr = open(path,'rb')
	data = fr.read()
	dataDecoded = base64.b64decode(data)
	fw = open(new_path, 'wb')
	fw.write(dataDecoded)
	fr.close()
	fw.close()


if len(sys.argv) != 3:
	print("Decode : {} d [path]".format(sys.argv[0]))
	print("Encode : {} e [path]".format(sys.argv[0]))
else:
	if sys.argv[1] == 'd':
		decodeFile(sys.argv[2])
	elif sys.argv[1] == 'e':
		encodeFile(sys.argv[2])