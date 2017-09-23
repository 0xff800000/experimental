import pygame
import random
import math,sys
import numpy as np

screenX,screenY = (400,400)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenX,screenY))
screenBox = pygame.Rect(0,0,screenX,screenY)
font = pygame.font.SysFont("monospace", 15)
deathCount = 0
sucessCount = 0

class Rocket:
	def __init__(self, coords, moves):
		self.x, self.y = coords
		self.speed = np.array([0.0,0.0])
		self.moves = moves
		self.currentMove = 0
		self.fitness = 0
		self.maxfit = 1000
		self.bestDist = 1e100
		self.isAlive = True
		self.isBest = False
		self.hitTarget = False
		self.lifeTime = 1
		self.longevity = 1e3
		self.maxSpeed = 1
		self.hitbox = pygame.Rect(self.x,self.y,5,5)
		self.image = pygame.Surface((5,15))

	def step(self,world,target):
		# Compute best distance to target
		currentDist = np.linalg.norm(np.array([target.x+target.w/2,target.y+target.h/2])-np.array([self.x,self.y]))
		if currentDist < self.bestDist:
			self.bestDist = currentDist
			self.fitness = (self.maxfit - self.bestDist) #* (self.longevity - self.lifeTime)
		if self.hitbox.colliderect(target):
			self.fitness = 1e100
			self.hitTarget = True
		# Clip to screen
		if not screenBox.contains(self.hitbox):
			self.isAlive = False
		# Check collision
		if self.hitbox.collidelist(world) != -1:
			self.isAlive = False
		# Check lifespan
		self.lifeTime += 1
		if self.lifeTime > self.longevity:
			self.isAlive = False
		# Move rocket
		if self.currentMove == len(self.moves): self.currentMove = 0
		if self.isAlive and not self.hitTarget:
			self.speed = np.add(self.moves[int(self.currentMove)],self.speed)
			self.currentMove += 0.01
			# Clip speed
			v = np.linalg.norm(self.speed)
			if v > self.maxSpeed:
				self.speed = self.speed / v
		else:
			self.speed = np.array([0,0])
		self.x += self.speed[0]
		self.y += self.speed[1]
		self.hitbox = pygame.Rect(self.x,self.y,5,5)
		# Draw rocket
		color = (0,255,0,128)
		if not self.isAlive:
			self.fitness = 0
			color = (255,0,0,128)
		if self.isBest:
			color = (0,0,255,128)
		angle = 0
		if np.linalg.norm(self.speed) > 0:
			angle = np.dot(self.speed,(1,0)) / (np.linalg.norm(self.speed))
		img = pygame.transform.rotate(self.image,angle)
		img.fill(color)
		screen.blit(img,(self.x,self.y))
	

class Population:
	def __init__(self,count,spawnPoint,target):
		self.count = count
		self.elitism = 0.3
		self.spawn = spawnPoint
		self.target = pygame.Rect(target,(50,50))
		self.maxMoves = 100
		self.mutations = 0.1
		self.obstacles = [pygame.Rect((200,0),(10,300))]
		self.rockets = []
		self.sucessGenes = []
		self.sucessGenesCount = 100
		for r in range(count):
			moves = [2*np.random.rand(2,)-np.array([1,1]) for x in range(self.maxMoves)]
			self.rockets.append(Rocket(self.spawn,moves))
	
	def update(self):
		global deathCount
		global sucessCount
		finishedRockets = [ x for x in self.rockets if not x.isAlive or x.hitTarget ]
		finishedRockets.sort(key=lambda f: f.fitness, reverse=True)
		for x in self.rockets:
			if x.hitTarget: self.sucessGenes.append(x)
		self.sucessGenes.sort(key=lambda f: f.lifeTime, reverse=False)
		while len(self.sucessGenes) > self.sucessGenesCount: self.sucessGenes.pop()
		for i,f in enumerate(self.rockets):
			f.step(self.obstacles,self.target)
			if len(self.sucessGenes)!=0: finishedRockets = self.sucessGenes
			if len(finishedRockets) != 0:
				parent1 = random.randint(0,int(self.elitism*len(finishedRockets)))
				parent2 = random.randint(0,int(self.elitism*len(finishedRockets)))
				genes1 = []; genes2 = []
				moves = []
				if not f.isAlive:
					deathCount += 1
					# Create new child from best specimens
					genes1 = self.rockets[parent1].moves
					genes2 = self.rockets[parent2].moves
				if f.hitTarget:
					sucessCount += 1
					genes1 = f.moves
					genes2 = self.rockets[parent2].moves
				if f.hitTarget or not f.isAlive:
					crossDNA = [ random.randint(0,1) for x in range(len(genes1)) ]
					# Cross parents
					for k,x in enumerate(crossDNA):
						if x == 0:
							moves.append(genes1[k])
						else:
							moves.append(genes2[k])
					
					# Mutate
					for x in range(int(self.mutations*self.maxMoves)):
						gene = random.randint(0,self.maxMoves-1)
						moves[gene] = 2*np.random.rand(2,)-np.array([1,1])
					self.rockets[i] = Rocket(self.spawn,moves)
				
		# Sort populaton according to fitness
		self.rockets.sort(key=lambda f: f.fitness, reverse=True)
		self.rockets[0].isBest = True
		# Draw target
		pygame.draw.rect(screen,(0,0,0),self.target)
		# Draw obstacles
		for o in self.obstacles:
			pygame.draw.rect(screen,(100,100,100),o)
		
popul = Population(100,(100,130),(300,50))

while True:
	screen.fill((255,255,255))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT: pygame.quit(); sys.exit()
		if event.type == pygame.KEYDOWN:
			key = pygame.key.get_pressed()
			if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
			if event.key == pygame.K_y: popul.mutations += 0.1
	popul.update()
	if deathCount != 0: sc = sucessCount/deathCount
	else: sc = sucessCount
	label = font.render('Death:{}; Sucess:{}; S/D={}'.format(deathCount,sucessCount,sc),1,(0,0,0))
	screen.blit(label, (10,10))
	# Render frame
	pygame.display.flip()
'''
	# Write info
	coords = ants[0].getCoords()
	label = font.render('{0:3.1f};{1:3.1f};{2:3.1f};{3}'.format(coords[0],coords[1],coords[2],ants[0].fitness),1,(0,0,0))
	screen.blit(label, (10,10))
'''
