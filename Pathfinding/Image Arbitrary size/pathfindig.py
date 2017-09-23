import pygame
import sys
from PIL import Image

################### Screen ###################

def drawPixel(coord,color):
    pygame.draw.rect(screen,color,(coord[0]*pW,coord[1]*pH,pW,pH))
    #pygame.display.flip()

def node2Pix(n):
    return (n%nW,int(n/nW))

def printPath(parent):
    currentPos=parent[target]
    while currentPos!=source:
        #print(currentPos)
        drawPixel(node2Pix(currentPos),(0,0,255))
        currentPos=parent[currentPos]
        pygame.display.flip()
    pygame.display.flip()

def printPath2(parent):
    currentPos=parent[source]
    while currentPos!=target:
        drawPixel(node2Pix(currentPos),(0,0,255))
        currentPos=parent[currentPos]
        pygame.display.flip()
    

# Create window
pygame.init()
# Load map
img = Image.open('map6.png')
# Pixels count
nW,nH = img.size[0],img.size[1]
# Window size
w,h = 5*nW,5*nH; pW,pH = w/nW,h/nH
screen = pygame.display.set_mode((w,h))
screen.fill((255,255,255))
pygame.display.flip()

################### Node ###################

vertex = []
for y in range(nH):
    for x in range(nW):
        vertex.append([])

################### Fill graph ###################

source=0; target=0

def lookPixels(x,y,pixels):
    return (pixels[x,y][0],pixels[x,y][1],pixels[x,y][2])

def registerVertex(v1,v2):
    if v2 not in vertex[v1]:vertex[v1].append(v2)
    if v1 not in vertex[v2]:vertex[v2].append(v1)

def fillGraph():
    WALK=(255,255,255)
    OBST=(0,0,0)
    SRC=(0,255,0)
    TGT=(255,0,0)
    pixels = img.load()
    i=0
    global target,source
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if lookPixels(x,y,pixels)==TGT: target=i; drawPixel((x,y),TGT); print('Target found at ({},{})'.format(x,y))
            if lookPixels(x,y,pixels)==SRC: source=i; drawPixel((x,y),SRC); print('Source found at ({},{})'.format(x,y))
            if lookPixels(x,y,pixels)!=OBST:
                # Looking E,S,W,N
                if x+1 in range(img.size[0]):
                    if lookPixels(x+1,y,pixels)!=OBST:
                        registerVertex(i,i+1)
                if y+1 in range(img.size[0]):
                    if lookPixels(x,y+1,pixels)!=OBST:
                       registerVertex(i,i+nW)
                if x-1 in range(img.size[0]):
                    if lookPixels(x-1,y,pixels)!=OBST:
                        registerVertex(i,i-1)
                if y-1 in range(img.size[0]):
                    if lookPixels(x,y-1,pixels)!=OBST:
                        registerVertex(i,i-nW)
            else:
                drawPixel((x,y),OBST)
            i+=1
    pygame.display.flip()
    
################### Pathfinding ###################

def BFS(ad,s):
    level={s:0}
    parent={s:None}
    i=1
    frontier=[s]
    while frontier:
        next=[]
        for u in frontier:
            for v in ad[u]:
                if v not in level:
                    level[v]=i
                    parent[v]=u
                    next.append(v)
        frontier=next
        i+=1

        # Target found
        if target in parent: break
    
    #print('Parent graph: {}'.format(parent))
    #print('Weight graph: {}'.format(level))
    return parent#,level

def getDist(n1,n2):
    d1=node2Pix(n1)
    d2=node2Pix(n2)
    return (d2[0]-d1[0])**2+(d2[1]-d1[1])**2

def AStar(ad,s):
    opened=[s]
    closed=[]
    f={s:0}
    g={s:0}
    h={}
    parents={}

    while opened:
        # Find least f for each opened
        q=0; minF=sys.maxsize
        for o in opened:
            if f[o]<minF: minF=f[o]; q=o
        # Pop it form opened
        opened.remove(q)
        # Get successors
        successor=ad[q]
        for succ in successor:
            # Set succssesor parent to q
            parents[succ]=q
            # If target reached set all nei parents
            if succ == target:
                surround=ad[succ]
                for su in surround:
                    parents[su]=succ
                return parents
            # Compute F,G,H cost 
            g[succ]=g[q]+1
            h[succ]=getDist(succ,target)
            f[succ]=g[succ]+h[succ]
            # Find if this succ has another opened
            skip1=False
            for su in successor:
                if su in opened and f[su]<f[succ]:skip1=True
            skip2=False
            for su in successor:
                if su in closed and f[su]<f[succ]:skip2=True
            if not skip1 and not skip2:
                opened.append(succ)
        # Close q
        closed.append(q)

################### Main ###################


fillGraph()
path=BFS(vertex,source)
printPath(path)
