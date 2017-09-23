import pygame, sys, math, random
from threading import Thread

renderPoly = False

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

'''
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
'''

def rotate2D(pos,rad):
    x,y=pos
    c,s = math.cos(rad),math.sin(rad)
    return x*c-y*s,y*c+x*s



class Cam:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos=list(pos)
        self.rot=list(rot)
    def events(self,event):
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

verts,face = importMesh('cube.obj')
#verts,face = importMeshScale('castle.obj',0.001)
colors = [(int(random.random()*255),int(random.random()*255),int(random.random()*255)) for x in range(len(face))]
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


def drawPoly():
    global renderPoly
    #print("poly\n")
    while True:
        if renderPoly:
            # Compute screen coords for each vertex
            
            screenCoord=[]
            for vertex in verts:
                screenCoord.append(getScreenCoord(vertex))
            colorIndex = 0
            for polygon in face:
                polyVerts = []
                zs = []
                for vertex in polygon:
                    sc,z = screenCoord[vertex]
                    polyVerts.append(sc)
                    zs.append(z)
                if max(zs)<0:
                    pygame.draw.polygon(screen,colors[colorIndex],polyVerts,0)
                colorIndex = colorIndex+1
            renderPoly = False

class thread(Thread):
    def __init__(self,func):
        Thread.__init__(self)
        self.task = func
    def run(self):
        #print("LOL")
        self.task()

# Main loop
wireRender=True
vertRender=True
polyRender=False

polyTh = thread(drawPoly)
#polyTh.run = drawPoly
polyTh.start()

#screen.fill((255,255,255))

while True:
    dt = clock.tick()/1000
    
    for event in pygame.event.get():
        updateScreen = False
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            updateScreen = True
            if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
            if event.key == pygame.K_x: wireRender=not wireRender
            if event.key == pygame.K_c: vertRender=not vertRender
            if event.key == pygame.K_y: polyRender=not polyRender
        if event.type == pygame.MOUSEMOTION:
            updateScreen = True
            cam.events(event)

    if updateScreen:
        screen.fill((255,255,255))

        if polyRender:renderPoly = True
        if vertRender:drawVert()
        if wireRender:drawLines()

        #if polyRender:polyTh.join()
    
    pygame.display.flip()

    key = pygame.key.get_pressed()
    cam.update(dt,key)
