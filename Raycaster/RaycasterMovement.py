import pygame, sys, math

def rotate2D(pos,rad):
    x,y=pos
    c,s = math.cos(rad),math.sin(rad)
    return x*c-y*s,y*c+x*s

class Cam:
    def __init__(self,pos=(0,0),rot=(0,0)):
        self.pos=list(pos)
        self.rot=list(rot)
        self.dir=rotate2D((0,10),-self.rot[0])

    def events(self,event):
        if event.type == pygame.MOUSEMOTION:
            x,y=event.rel
            x/=200; y/=200
            self.rot[0]-=x; self.rot[1]+=y
            self.dir=rotate2D((0,10),-self.rot[0])

    def update(self,dt,key):
        s=dt*10
        # movement in relative directions
        x,y = s*math.sin(self.rot[0]), s*math.cos(self.rot[0])
        if key[pygame.K_w]: self.pos[0]+=x;self.pos[1]+=y
        if key[pygame.K_s]: self.pos[0]-=x;self.pos[1]-=y
        if key[pygame.K_d]: self.pos[0]-=y;self.pos[1]+=x
        if key[pygame.K_a]: self.pos[0]+=y;self.pos[1]-=x

pygame.init()
w,h = 400,400; cx,cy = w//2,h//2
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

# Map
mapPts = [(-50,-50),(50,-50),(50,50),(-50,50),(-50,-50)]
for i,pt in enumerate(mapPts):
    print(i,pt)
    mapPts[i] = (pt[0]+w/2,pt[1]+h/2)

cam = Cam((w/2,h/2))

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

    # Draw 2D map
    for pt in range(len(mapPts)-1):
        pygame.draw.line(screen,(0,0,0),mapPts[pt],mapPts[pt+1],1)

    # Draw player
    pygame.draw.circle(screen, (0,0,0), (int(cam.pos[0]),int(cam.pos[1])),3)
    pygame.draw.line(screen,(0,0,0),(int(cam.pos[0]),int(cam.pos[1])),(int(cam.pos[0]+cam.dir[0]),int(cam.pos[1]+cam.dir[1])),1)

    #pygame.draw.line(screen,(0,0,0),points[0],points[1],1)

    pygame.display.flip()

    key = pygame.key.get_pressed()
    cam.update(dt,key)
