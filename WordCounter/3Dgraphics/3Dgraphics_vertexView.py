import pygame, sys, math

def importMesh(file):
    vertex=[]
    f=open(file,'r')
    for line in f:
        line=line.split()
        if line[0]=='v':
            vertex.append((float(line[1]),float(line[2]),float(line[3])))
    return vertex

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

verts = importMesh('ape2.obj')
lines = (0,1),(0,3),(0,4),(1,2),(1,4),(2,3),(2,4),(3,4)

cam = Cam((0,0,-5))

pygame.event.get(); pygame.mouse.get_rel()
pygame.mouse.set_visible(0); pygame.event.set_grab(1)

while True:
    dt = clock.tick()/1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
        cam.events(event)

    screen.fill((255,255,255))

    it=0
    
    for x,y,z in verts:
        it+=1
        x+=cam.pos[0]
        y+=cam.pos[1]
        z+=cam.pos[2]
        x,z=rotate2D((x,z),cam.rot[0])
        y,z=rotate2D((y,z),cam.rot[1])
        if z!=0: f = 200/z
        x,y = x*f, y*f
        pygame.draw.circle(screen,(0,0,0),(cx+int(x),cy+int(y)),3)
        if it==1 or it==13 or it==14 or it==2:pygame.draw.circle(screen,(255,0,0),(cx+int(x),cy+int(y)),6)

    pygame.display.flip()

    key = pygame.key.get_pressed()
    cam.update(dt,key)
