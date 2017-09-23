import pygame, sys, math

class Cam:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos=list(pos)
        self.rot=list(rot)

    def update(self,dt,key):
        s=dt*10
        if key[pygame.K_w]: self.pos[2]+=s
        if key[pygame.K_a]: self.pos[0]+=s
        if key[pygame.K_s]: self.pos[2]-=s
        if key[pygame.K_d]: self.pos[0]-=s
        if key[pygame.K_q]: self.pos[1]-=s
        if key[pygame.K_e]: self.pos[1]+=s

pygame.init()
w,h = 400,400; cx,cy = w//2,h//2
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

verts = (-1,1,-1),(1,1,-1),(1,-1,-1),(-1,-1,-1),(-1,-1,1)
lines = (0,1),(0,3),(0,4),(1,2),(1,4),(2,3),(2,4),(3,4)

cam = Cam((0,0,-5))

while True:
    dt = clock.tick()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit; sys.exit()

    screen.fill((255,255,255))

    for line in lines:
        points=[]
        for x,y,z in (verts[line[0]],verts[line[1]]):
            x+=cam.pos[0]
            y+=cam.pos[1]
            z+=cam.pos[2]
            if z!=0: f = 200/z
            x,y = x*f, y*f
            points+=[(cx+int(x),cy+int(y))]
        pygame.draw.line(screen,(0,0,0),points[0],points[1],1)

    pygame.display.flip()

    key = pygame.key.get_pressed()
    cam.update(dt,key)
