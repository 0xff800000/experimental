
lineStr = '<draw:line draw:style-name=\"gr1\" draw:text-style-name=\"P1\" draw:layer=\"layout\" svg:x1=\"{}cm\" svg:y1=\"{}cm\" svg:x2=\"{}cm\" svg:y2=\"{}cm\"><text:p/></draw:line>'
endStr = '</draw:page></office:drawing></office:body></office:document>'

def importMesh(objPath,scale=1):
    vertex=[]
    faces=[]
    f=open(objPath,'r')
    for line in f:
        if len(line)>3:
            line=line.replace('/',' ')
            line=line.split()
            if line[0]=='v':
                vertex.append(((float(line[1]))*scale,(float(line[2]))*scale,(float(line[3]))*scale))
            elif line[0]=='f':
                polygon=[]
                for i in range(1,len(line),2):
                    polygon.append(int(line[i])-1)
                polygon.append(polygon[0])
                faces.append(polygon)
    return vertex,faces

cx,cy = 20,20
pos = (0,0,-5)
verts,face = importMesh('calib.obj',1)

def getScreenCoord(vertex):
    x,y,z=vertex[0],vertex[1],vertex[2]
    x+=pos[0]
    y+=pos[1]
    z+=pos[2]
    # x,z=rotate2D((x,z),cam.rot[0])
    # y,z=rotate2D((y,z),cam.rot[1])
    f = 1/-z
    x,y = x*f, -y*f#; x+=cx; y+=cy
    return ((x,y,z))

def renderMesh(outPath):
    # Read header
    header = open('header.txt','r').read()

    # Open output file
    f = open(outPath,'w')
    f.write(header)

    # Convert 3D to 2D
    screenCoord = []
    for vertex in verts:
        screenCoord.append(getScreenCoord(vertex))

    # Parse faces
    drawnLines = []
    for polygon in range(len(face)-1):
        for i in range(len(face[polygon])-1):
            #print(screenCoord[face[polygon][i]][0])
            #if screenCoord[face[polygon][i]][2]<0 and screenCoord[face[polygon][i+1]][2]<0:
            tst1 = screenCoord[face[polygon][i]][2]/abs(screenCoord[face[polygon][i]][2])
            tst2 = screenCoord[face[polygon][i+1]][2]/abs(screenCoord[face[polygon][i+1]][2])
            p1,p2 = face[polygon][i],face[polygon][i+1]
            if tst1 == tst2 and (p1,p2) not in drawnLines:
                #pygame.draw.line(screen,(0,0,0),screenCoord[face[polygon][i]],screenCoord[face[polygon][i+1]],1)
                drawnLines.append((p1,p2))
                drawnLines.append((p2,p1))
                x1=screenCoord[face[polygon][i]][0]
                y1=screenCoord[face[polygon][i]][1]
                x2=screenCoord[face[polygon][i+1]][0]
                y2=screenCoord[face[polygon][i+1]][1]
                f.write(lineStr.format(x1,y1,x2,y2))

    f.write(endStr)

renderMesh('a.fodg')