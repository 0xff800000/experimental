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
		self.lifeTime = 0
		self.longevity = 1e4
		self.maxSpeed = 1
		self.hitbox = pygame.Rect(self.x,self.y,5,5)
		self.image = pygame.Surface((5,15))

	def step(self,world,target):
		# Compute best distance to target
		currentDist = np.linalg.norm(np.array([target.x,target.y])-np.array([self.x,self.y]))
		if currentDist < self.bestDist:
			self.bestDist = currentDist
			self.fitness = (self.maxfit - self.bestDist) * (self.longevity - self.lifeTime)
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
		if self.isAlive:
			self.speed = np.add(self.moves[self.currentMove],self.speed)
			self.currentMove += 1
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
		self.elitism = int(0.3*count)
		self.spawn = spawnPoint
		self.target = pygame.Rect(target,(10,10))
		self.maxMoves = 1000
		self.mutations = int(0.1*self.maxMoves)
		self.rockets = []
		for r in range(count):
			moves = [2*np.random.rand(2,)-np.array([1,1]) for x in range(self.maxMoves)]
			self.rockets.append(Rocket(self.spawn,moves))
	
	def update(self):
		global deathCount
		for i,f in enumerate(self.rockets):
			f.step([],self.target)
			if not f.isAlive:
				deathCount += 1
				# Create new child from best specimens
				parent1 = random.randint(0,self.elitism)
				parent2 = random.randint(0,self.elitism)
				genes1 = self.rockets[parent1].moves
				genes2 = self.rockets[parent2].moves
				crossDNA = [ random.randint(0,1) for x in range(len(genes1)) ]
				moves = []
				for k,x in enumerate(crossDNA):
					if x == 0:
						moves.append(genes1[k])
					else:
						moves.append(genes2[k])
				self.rockets[i] = Rocket(self.spawn,moves)
			if f.hitTarget:
				genes1 = f.moves
				parent2 = random.randint(0,self.elitism)
				genes2 = self.rockets[parent2].moves
				crossDNA = [ random.randint(0,1) for x in range(len(genes1)) ]
				moves = []
				for k,x in enumerate(crossDNA):
					if x == 0:
						moves.append(genes1[k])
					else:
						moves.append(genes2[k])
				self.rockets[i] = Rocket(self.spawn,moves)
				
		# Sort populaton according to fitness
		self.rockets.sort(key=lambda f: f.fitness, reverse=True)
		self.rockets[0].isBest = True
		# Draw target
		pygame.draw.rect(screen,(0,0,0),self.target)
		
popul = Population(100,(100,130),(300,300))

while True:
	screen.fill((255,255,255))
	
	key = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.QUIT: pygame.quit(); sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
	
	popul.update()
	label = font.render('Death:{}; Best:{}'.format(deathCount,popul.rockets[0].fitness),1,(0,0,0))
	screen.blit(label, (10,10))
	# Render frame
	pygame.display.flip()
'''
	# Write info
	coords = ants[0].getCoords()
	label = font.render('{0:3.1f};{1:3.1f};{2:3.1f};{3}'.format(coords[0],coords[1],coords[2],ants[0].fitness),1,(0,0,0))
	screen.blit(label, (10,10))
'''
