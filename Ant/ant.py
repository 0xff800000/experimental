import pygame
import random
import math,sys

screenX,screenY = (400,400)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenX,screenY))
antImage = pygame.image.load("ant.gif")
antSprite = antImage.get_rect()
font = pygame.font.SysFont("monospace", 15)

class Food:
	def __init__(self, nb):
		self.size = 4
		self.count = nb
		self.foodArray = [ (random.randint(0,screenX-self.size),random.randint(0,screenY-self.size),True) for i in range(self.count) ]
		self.hitboxes = [pygame.Rect(f[0],f[1],self.size,self.size) for f in self.foodArray]
	
	def update(self):
		for i,f in enumerate(self.foodArray):
			# If the food is eaten, generate new one
			if f[2] == False:
				x,y = (random.randint(0,screenX-self.size),random.randint(0,screenY-self.size))
				self.foodArray[i] = (x,y,True)
				self.hitboxes[i] = pygame.Rect(x,y,self.size,self.size)
			# Draw food
			pygame.draw.rect(screen, (0,255,0), self.hitboxes[i])
	
	def eat(self,i):
		if i in range(len(self.foodArray)):
			x,y,t = self.foodArray[i]
			self.foodArray[i] = (x,y,False)
		
class Ant:
	def __init__(self, coords):
		self.x, self.y, self.angle = coords
		self.speed = 1
		self.turnRate = 0.01
		self.fitness = 0
		self.size = 8
		self.hitbox = pygame.Rect(self.x,self.y,self.size,self.size)
		sensor = pygame

	def step(self,dt,food):
		a = math.radians(self.angle)
		self.x += self.speed * math.cos(a)*dt
		self.y += self.speed * math.sin(a)*dt
		self.hitbox = pygame.Rect(self.x,self.y,self.size,self.size)
		# Clip to screen
		if self.x > screenX: self.x = screenX
		if self.y > screenY: self.y = screenY
		if self.x < 0: self.x = 0
		if self.y < 0: self.y = 0
		# Eat food
		for i,f in enumerate(food.hitboxes):
			if self.hitbox.colliderect(f):
				self.fitness += 1
				food.eat(i)

	def turnLeft(self):
		if self.angle > 360:
			self.angle = 0
		else: self.angle += self.turnRate

	def turnRight(self):
		if self.angle < 0:
			self.angle = 360
		else: self.angle -= self.turnRate
        
	def getCoords(self):
		return (self.x, self.y, self.angle)

def drawAnts(colony):
	for a in colony:
		img = pygame.transform.rotate(antImage,a.angle)
		screen.blit(img,(a.x,a.y))

ants = []
ants.append(Ant((50,50,90)))
ants.append(Ant((250,150,30)))
clkDiv = 100
food = Food(100)

while True:
	screen.fill((255,255,255))
	dt = clock.tick()/clkDiv
	key = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.QUIT: pygame.quit(); sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
		if key[pygame.K_y]: clkDiv *= 10
		if key[pygame.K_x]: clkDiv /= 10
	if key[pygame.K_a]: ants[0].turnLeft();
	if key[pygame.K_d]: ants[0].turnRight();
	for a in ants: a.step(dt,food)
	food.update()
	drawAnts(ants)
	
	# Write info
	coords = ants[0].getCoords()
	label = font.render('{0:3.1f};{1:3.1f};{2:3.1f};{3}'.format(coords[0],coords[1],coords[2],ants[0].fitness),1,(0,0,0))
	screen.blit(label, (10,10))
	# Render frame
	pygame.display.flip()
'''
	for a in ants:
		if bool(random.getrandbits(1)):
			a.turnLeft()
		else:
			a.turnRight()
		a.step(dt)
'''