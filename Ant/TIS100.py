import pygame
import random
import math,sys

screenX,screenY = (400,400)
pygame.init()
screen = pygame.display.set_mode((screenX,screenY))
antImage = pygame.image.load("ant.gif")
antSprite = antImage.get_rect()

class Ant:
	def __init__(self, coords):
		self.x, self.y, self.angle = coords
		self.speed = 1

	def step(self):
		self.x += self.speed * math.cos(self.angle)
		self.y += self.speed * math.sin(self.angle)
		if self.x > screenX:
			self.x = screenX
		if self.y > screenY:
			self.y = screenY
		if self.x < 0:
			self.x = 0
		if self.y < 0:
			self.y = 0

	def turnLeft(self):
		if self.angle == 360:
			self.angle = 0
		else: self.angle += 1

	def turnRight(self):
		if self.angle == 0:
			self.angle = 360
		else: self.angle -= 1
        
	def getCoords(self):
		return (self.x, self.y, self.angle)

def drawAnts(colony):
	screen.fill((255,255,255))
	for a in colony:
		img = pygame.transform.rotate(antImage,a.angle)
		screen.blit(img,(a.x,a.y))
	pygame.display.flip()

ants = []
ants.append(Ant((50,50,90)))
ants.append(Ant((250,150,30)))

while True:
	for a in ants:
		if bool(random.getrandbits(1)):
			a.turnLeft()
		else:
			a.turnRight()
		a.step()
	drawAnts(ants)
	for event in pygame.event.get():
		if event.type == pygame.QUIT: pygame.quit(); sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
