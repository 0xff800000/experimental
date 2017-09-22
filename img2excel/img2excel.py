from PIL import Image

spreadSheetH = 1
spreadSheetW = 1

fileHeader = open('header.txt','r').read()

styleStr = '<Style ss:ID=\"{}\"><Interior ss:Color=\"#{:02x}{:02x}{:02x}\" ss:Pattern=\"Solid\"/></Style>\n'
styleEnd = '</Styles>'

rowBegin = '<Row ss:AutoFitHeight="0" ss:Height="{}">'
rowEnd = '</Row>'

columnStr = '<ss:Worksheet ss:Name=\"Sheet1\"><Table ss:StyleID=\"ta1\"><Column ss:Span=\"{}\" ss:Width=\"{}\"/>'

cellStr = '<Cell ss:StyleID=\"{}\"/>'

fileEnd = '</Table><x:WorksheetOptions/></ss:Worksheet></Workbook>'

def convertImage(imgPath,outPath):
	# Load image
	img=Image.open(imgPath)
	pixels = img.load()

	# Load file
	f=open(outPath,'w')
	f.write(fileHeader)

	# Write the color table
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			p = pixels[(x,y)]
			r,g,b = pixels[(x,y)]
			f.write(styleStr.format(str(p),r,g,b))
	f.write(styleEnd)
	f.write('\n\n')

	# Write column span and width
	f.write(columnStr.format(img.size[0],spreadSheetW))

	# Parse image
	for y in range(img.size[1]):
		f.write(rowBegin.format(spreadSheetH))
		for x in range(img.size[0]):
			p = pixels[(x,y)]
			f.write(cellStr.format(str(p)))
		f.write(rowEnd)

	# End file
	f.write(fileEnd)



convertImage('g.jpg','out.xml')