import pygame, sys, math

def importMesh(file):
    vertex=[]
    faces=[]
    f=open(file,'r')
    for line in f:
        if len(line)>3:
            line=line.replace('/',' ')
            line=line.split()
            if line[0]=='v':
                vertex.append((float(line[1]),float(line[2]),float(line[3])))
            elif line[0]=='f':
                polygon=[]
                for i in range(1,len(line),2):
                    polygon.append(int(line[i])-1)
                polygon.append(polygon[0])
                faces.append(polygon)
    return vertex,faces

def importMeshScale(file,scale):
    vertex=[]
    faces=[]
    f=open(file,'r')
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



def rotate2D(pos,rad):
    x,y=pos
    c,s = math.cos(rad),math.sin(rad)
    return x*c-y*s,y*c+x*s



class Cam:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos=list(pos)
        self.rot=list(rot)
    def events(self,event):
        if event.type == pygame.MOUSEMOTION:
            x,y=event.rel
            x/=200; y/=200
            self.rot[0]+=x; self.rot[1]+=y
    def update(self,dt,key):
        s=dt*10
        # movement in relative directions
        x,y = s*math.sin(self.rot[0]), s*math.cos(self.rot[0])
        if key[pygame.K_w]: self.pos[0]+=x;self.pos[2]+=y
        if key[pygame.K_s]: self.pos[0]-=x;self.pos[2]-=y
        if key[pygame.K_d]: self.pos[0]+=y;self.pos[2]-=x
        if key[pygame.K_a]: self.pos[0]-=y;self.pos[2]+=x

        
        if key[pygame.K_q]: self.pos[1]-=s
        if key[pygame.K_e]: self.pos[1]+=s

pygame.init()
w,h = 400,400; cx,cy = w//2,h//2
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

verts,face = importMesh('ape2.obj')
#verts,face = importMeshScale('castle.obj',0.001)

cam = Cam((0,0,-5))

pygame.event.get(); pygame.mouse.get_rel()
pygame.mouse.set_visible(0); pygame.event.set_grab(1)

def drawVert():
    for vertex in verts:
        screenXY,z=getScreenCoord(vertex)
        if z<0:
            try:
                pygame.draw.circle(screen,(0,0,0),screenXY,2)
            except:
                print('Convert error')

'''
def drawVert():
    for x,y,z in verts:
        x+=cam.pos[0]
        y+=cam.pos[1]
        z+=cam.pos[2]
        x,z=rotate2D((x,z),cam.rot[0])
        y,z=rotate2D((y,z),cam.rot[1])
        if z!=0: f = 200/z
        x,y = x*f, y*f
        pygame.draw.circle(screen,(0,0,0),(cx+int(x),cy+int(y)),2)
'''

def getScreenCoord(vertex):
    x,y,z=vertex[0],vertex[1],vertex[2]
    x+=cam.pos[0]
    y+=cam.pos[1]
    z+=cam.pos[2]
    x,z=rotate2D((x,z),cam.rot[0])
    y,z=rotate2D((y,z),cam.rot[1])
    f = 200/z
    x,y = x*f, y*f; x+=cx; y+=cy
    return (int(x),int(y)),z

def drawLines():
    # Compute screen coords for each vertex
    screenCoord=[]
    intersect=[]
    for vertex in verts:
        screenCoord.append(getScreenCoord(vertex))
    for polygon in range(len(face)-1):
        for i in range(len(face[polygon])-1):
            pt1,z1 = screenCoord[face[polygon][i]]
            pt2,z2 = screenCoord[face[polygon][i+1]]
            if z1<0 and z2<0:
                try:
                    pygame.draw.line(screen,(0,0,0),pt1,pt2,1)
                except:
                    print('Line error')

'''
def getScreenCoord(vertex):
    x,y,z=vertex[0],vertex[1],vertex[2]
    x+=cam.pos[0]
    y+=cam.pos[1]
    z+=cam.pos[2]
    x,z=rotate2D((x,z),cam.rot[0])
    y,z=rotate2D((y,z),cam.rot[1])
    if z<0:
        f = 200/z
        x,y = x*f, y*f; x+=cx; y+=cy
        return (int(x)),(int(y))
    else: return -1,-1

def drawLines():
    # Compute screen coords for each vertex
    screenCoord=[]
    intersect=[]
    for vertex in verts:
        screenCoord.append(getScreenCoord(vertex))
    for polygon in range(len(face)-1):
        for i in range(len(face[polygon])-1):
            pygame.draw.line(screen,(0,0,0),screenCoord[face[polygon][i]],screenCoord[face[polygon][i+1]],1)
'''
'''
def drawLines():
    # Compute screen coords for each vertex
    screenCoord=[]
    for vertex in verts:
        screenCoord.append(getScreenCoord(vertex))
    for polygon in range(len(face)-1):
        for i in range(len(face[polygon])-1):
            pygame.draw.line(screen,(0,0,0),screenCoord[face[polygon][i]],screenCoord[face[polygon][i+1]],1)

def drawLines():
    for polygon in range(len(face)-1):
        #face[polygon].append(face[polygon][0])
        #print(face[polygon])
        for i in range(len(face[polygon])-2):
            #print('{}, {}'.format(verts[face[polygon][i]],verts[face[polygon][i+1]]))
            points=[]
            for x,y,z in (verts[face[polygon][i]],verts[face[polygon][i+1]]):
                x+=cam.pos[0]
                y+=cam.pos[1]
                z+=cam.pos[2]
                x,z=rotate2D((x,z),cam.rot[0])
                y,z=rotate2D((y,z),cam.rot[1])
                if z!=0: f = 200/z
                x,y = x*f, y*f
                points+=[(cx+int(x),cy+int(y))]
            pygame.draw.line(screen,(0,0,0),points[0],points[1],1)
        #print(polygon)

def getScreenCoord(vertex):
    x,y,z=vertex[0],vertex[1],vertex[2]
    x+=cam.pos[0]
    y+=cam.pos[1]
    z+=cam.pos[2]
    x,z=rotate2D((x,z),cam.rot[0])
    y,z=rotate2D((y,z),cam.rot[1])
    if z!=0: f = 200/z
    x,y = x*f, y*f
    return (cx+int(x)),(cy+int(y))
'''

# Main loop
wireRender=True
vertRender=True

while True:
    dt = clock.tick()/1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
            if event.key == pygame.K_x: wireRender=not wireRender
            if event.key == pygame.K_c: vertRender=not vertRender
        cam.events(event)

    screen.fill((255,255,255))

    if vertRender:drawVert()
    if wireRender:drawLines()
    
    pygame.display.flip()

    key = pygame.key.get_pressed()
    cam.update(dt,key)
