import pygame
import sys
from tkinter.filedialog import askopenfilename
#import time
from PIL import Image

################### Screen ###################

def drawPixel(coord,color):
    pygame.draw.rect(screen,color,(coord[0]*pW,coord[1]*pH,pW,pH))
    #pygame.display.flip()

def node2Pix(n):
    return (n%nW,int(n/nW))

def printPath(parent):
    if target not in parent: print('Target unreachable.'); return
    currentPos=parent[target]
    while currentPos!=source:
        drawPixel(node2Pix(currentPos),(0,0,255))
        currentPos=parent[currentPos]
    pygame.display.flip()

def printPath2(parent):
    clock=pygame.time.Clock()
    currentPos=parent[target]
    while currentPos!=source:
        drawPixel(node2Pix(currentPos),(0,0,255))
        currentPos=parent[currentPos]
        pygame.display.flip()
        pygame.event.get()
        clock.tick(50)

def removePath():
    screen.fill((255,255,255))
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            drawPixel((x,y),lookPixels(x,y,imgPix))
    pygame.display.flip()

################### Node ###################
def vertexInit():
    ve = []
    for y in range(nH):
        for x in range(nW):
            ve.append([])
    return ve

################### Fill graph ###################

source=0; target=0

def lookPixels(x,y,pixels):
    return (pixels[x,y][0],pixels[x,y][1],pixels[x,y][2])

def registerVertex(v1,v2):
    if v2 not in vertex[v1]:vertex[v1].append(v2)
    if v1 not in vertex[v2]:vertex[v2].append(v1)

def fillGraph():
    screen.fill((255,255,255))
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

def fillGraph2():
    WALK=(255,255,255)
    OBST=(0,0,0)
    SRC=(0,255,0)
    TGT=(255,0,0)
    i=0
    global target,source,imgPix
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if lookPixels(x,y,imgPix)==TGT: target=i; drawPixel((x,y),TGT); print('Target found at ({},{}) {}'.format(x,y,i))
            if lookPixels(x,y,imgPix)==SRC: source=i; drawPixel((x,y),SRC); print('Source found at ({},{}) {}'.format(x,y,i))
            if lookPixels(x,y,imgPix)!=OBST:
                # Looking E,S,W,N
                if x+1 in range(img.size[0]):
                    if lookPixels(x+1,y,imgPix)!=OBST:
                        registerVertex(i,i+1)
                if y+1 in range(img.size[0]):
                    if lookPixels(x,y+1,imgPix)!=OBST:
                       registerVertex(i,i+nW)
                if x-1 in range(img.size[0]):
                    if lookPixels(x-1,y,imgPix)!=OBST:
                        registerVertex(i,i-1)
                if y-1 in range(img.size[0]):
                    if lookPixels(x,y-1,imgPix)!=OBST:
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
        if target in frontier: break
    
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

    while len(opened):
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
            '''
            if succ not in g or f[succ] < g[succ]:
                g[succ] = f[succ]

            '''
            # Find if this succ has another opened
            skip1=False
            for su in successor:
                if su in opened and f[su]<f[succ]:skip1=True
            skip2=False
            for su in successor:
                if su in closed and f[su]<f[succ]:skip2=True
            if not skip1 and not skip2:
                if succ not in opened: opened.append(succ)
        # Close q
        closed.append(q)

def a_star_search(graph, start):
    frontier = []
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

################### Main ###################

# Create window
pygame.init()
# Load map
mapPath = askopenfilename()
img = Image.open(mapPath)
# Pixels count
nW,nH = img.size[0],img.size[1]
# Window size
w,h = 5*nW,5*nH; pW,pH = w/nW,h/nH
screen = pygame.display.set_mode((w,h))
screen.fill((255,255,255))
pygame.display.flip()

imgPix=img.load()
cursorColor = (0,0,0)
vertex=vertexInit()
fillGraph2()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
            # Q : target
            if event.key == pygame.K_q: cursorColor=(255,0,0)
            # W : obstacle
            if event.key == pygame.K_w: cursorColor=(0,0,0)
            # E : void
            if event.key == pygame.K_e: cursorColor=(255,255,255)
            # R : source
            if event.key == pygame.K_r: cursorColor=(0,255,0)
            # A : fillgraph
            if event.key == pygame.K_a: img = Image.open(mapPath); imgPix=img.load(); screen.fill((255,255,255)); vertex=vertexInit(); fillGraph2()
            # S : clear path
            if event.key == pygame.K_s: removePath()
            # T : solve
            if event.key == pygame.K_t:
                vertex=[]
                vertex=vertexInit()
                fillGraph2()
                path=BFS(vertex,source)
                printPath(path)

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            b1,b2,b3=pygame.mouse.get_pressed()
            if b1 or b3:
                x,y=pygame.mouse.get_pos()
                x = int(x / w *nW)
                y = int(y / h *nH)
                #print((x,y))
                if b1: drawPixel((x,y),cursorColor); imgPix[x,y]=cursorColor
                if b3: drawPixel((x,y),(255,255,255)); imgPix[x,y]=(255,255,255)
                pygame.display.flip()
