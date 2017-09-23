import pyPdf

def getPDF(path):
	content = ""
	pdf = pyPdf.PdfFileReader(file(path,"rb"))
	for i in range(0,pdf.getNumPages()):
		content+=pdf.getPage(i).extractText()
	return content