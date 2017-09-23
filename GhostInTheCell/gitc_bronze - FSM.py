import sys, math
from enum import Enum

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
factory_dist = {}


def printf(s):
	print(s,file=sys.stderr)

class State(Enum):
	conquer_free = 0
	build_army = 1
	prepare_attack = 2
	attack = 3

	
def get_my(fact):
	return [f for f in fact if f[1]==1]

def get_enemy(fact):
	return [f for f in fact if f[1]==-1]
	
def get_avail(fact):
	return [f for f in fact if f[1]==0]

def get_useful(fact):
	return [f for f in fact if f[3]!=0]

def get_treat(fact,units):
	treatFact = []
	for f in fact:
		enemies=0
		time=0
		for u in units:
			if u[3] == f[0]:
				enemies += u[4]
				time += u[5]
		if enemies >= f[3]*time+f[2]:
			treatFact.append(f)
	return treatFact

def get_overpopulated(fact,units,unitThres):
	overPop=[]
	for f in fact:
		unitCount=f[2]
		for u in units:
			if u[3] == f[0]:
				unitCount += u[4]
		if unitCount >= unitThres:
			overPop.append(f)
	return overPop

def get_underpopulated(fact,units,unitThres):
	underPop=[]
	for f in fact:
		unitCount=f[2]
		for u in units:
			if u[3] == f[0]:
				unitCount += u[4]
		if unitCount < unitThres:
			underPop.append(f)
	return underPop

def get_units_count(facts,units):
	sumUnits=0
	for f in facts:
		sumUnits+=f[2]
	for u in units:
		sumUnits+=u[4]
	return sumUnits

def get_distance_sorted(fact,factories):
	fact_dist = factories
	fact_dist.sort(key=lambda x: factory_dist[(fact[0],x[0])])
	return fact_dist

def get_sorted_enemies(enemyFactories,enemyUnits):
	fact = []
	for f in enemyFactories:
		units=f[2]
		for u in enemyUnits:
			if u[3] == f[0]:
				units += u[4]
		fact.append((f,units))
	fact.sort(key=lambda x: x[1])
	return [f[0] for f in fact]

def ready_to_attack(fact,units):
	ready = True
	allUnits = get_units_count(fact,units)
	threshold = int(allUnits * 0.5)
	units_per_factories=[]
	for f in fact:
		unitFact = f[2]
		for u in units:
			if u[3] == f[0]:
				unitFact += u[4]
		units_per_factories.append(unitFact)
	for i in units_per_factories:
		if int(allUnits/len(fact))-threshold > i:
			ready = False
	return ready
	
def targeted_bomb(fact,bombs):
	targets = []
	for b in bombs:
		for f in fact:
			if b[3] == f[0]:
				targets.append(f)
	return targets

def get_neighbour(fact,factories,n=4):
	return get_distance_sorted(fact,factories)[:n]

def get_build_power(fact):
	power = 0
	for f in fact:
		power += f[3]
	return power

def get_req_attack_power(fact,units,enemy=False):
	allies = fact[2]
	enemies = 0
	time = 0
	entity = 1
	if enemy == True: entity = -1
	for u in units:
		if u[3] == fact[0]:
			if u[1] == entity:
				# Incoming allies
				allies += u[4]
			elif u[1] == -entity:
				# Incoming enemies
				enemies += u[4]
				time += u[5]
	#allies += time*fact[3]
	#printf('{},a:{},e:{}'.format(fact[0],allies,enemies))
	allies-=enemies
	return allies

class Conqueror():
	def __init__(self):
		self.state = State.conquer_free
		self.next_state = State.conquer_free
		self.commands = []

		self.build_power = 0
		self.enemy_build_power = 0
		self.found_target = False
		self.power_attack_factory = 0
		self.power_target_factory = 0
		self.power_factor = 1.1

		self.minimumBuildPower = 1

		self.targeted_factory = ()
		self.attack_point = ()

		self.myFactories = []
		self.myUnits = []
		self.myBombs = []

		self.enemyFactories = []
		self.enemyUnits = []
		self.enemyBombs = []

	def update_info(self,info):
		self.commands = []
		self.factories,self.units,self.bombs = info

		self.myFactories = get_my(self.factories)
		self.myUnits = get_my(self.units)
		self.myBombs = get_my(self.bombs)

		self.enemyFactories = get_enemy(self.factories)
		self.enemyUnits = get_enemy(self.units)
		self.enemyBombs = get_enemy(self.bombs)

		self.build_power = get_build_power(self.myFactories)
		self.enemy_build_power = get_build_power(self.enemyFactories)
		
		printf('Build pow:a={};b={}'.format(self.build_power,self.enemy_build_power))

		self.FSM_run()

		# Print orders
		if len(self.commands)>1:
			print(';'.join(self.commands))
		elif len(self.commands)==1:
			print(self.commands[0])
		else:
			print('WAIT')

	def defend(self):
		# Defence against units
		treatened_factories = [f for f in self.myFactories if get_req_attack_power(f,self.units)<0]
		treatened_factories = get_useful(treatened_factories)
		printf('Treat. factories:'+str(treatened_factories))
		for f in treatened_factories:
			attackRequired = get_req_attack_power(f,self.units)
			nei = get_neighbour(f,self.myFactories)
			for n in nei:
				attack = get_req_attack_power(n,self.units)
				if attack > 0:
					self.commands.append('MOVE {} {} {}'.format(n[0],f[0],int(attack)))
		# Defence against bombs
		targetedFact = targeted_bomb(self.myFactories,self.bombs)
		if len(targetedFact)!=0:
			for f in targetedFact:
				for b in self.bombs:
					if b[3]==f[0] and b[4] < 2:
						nei = get_neighbour(f,self.myFactories+get_avail(self.factories))
						if len(nei)!=0:self.commands.append('MOVE {} {} {}'.format(f[0],nei[0],f[2]))

	def upgrade(self):
		for f in self.myFactories:
			attackF = get_req_attack_power(f,self.units)
			if f[3] < 3:
				if attackF-10 > 0:
					self.commands.append('INC {}'.format(f[0]))
				else:
					nei = get_neighbour(f,self.myFactories)
					for n in nei:
						attackN = get_req_attack_power(n,self.units)
						if attackN-10 > 0:
							self.commands.append('MOVE {} {} {}'.format(n[0],f[0],10))

	def conquer_adj(self):
		# Conquer useful
		for f in self.myFactories:
			nei = get_neighbour(f,self.factories,4)
			nei = get_avail(nei)
			nei =get_useful(nei)
			if len(nei)==0: break
			target = nei[0]
			attack = get_req_attack_power(f,self.units)
			if attack-target[2] > 0:
				self.commands.append('MOVE {} {} {}'.format(f[0],target[0],attack))
				return
		# Convert useless
		for f in self.myFactories:
			nei = get_neighbour(f,self.factories,4)
			nei = get_avail(nei)
			if len(nei)==0: break
			target = nei[0]
			attack = get_req_attack_power(f,self.units)
			if attack-target[2] > 0:
				self.commands.append('MOVE {} {} {}'.format(f[0],target[0],attack))
				return

	def find_target(self):
		if self.build_power < self.enemy_build_power:
			self.found_target = False
			self.targeted_factory = ()
		useful_avail = get_useful(get_avail(self.factories))
		printf(useful_avail)
		if len(useful_avail)==0: useful_avail = self.enemyFactories
		for f in useful_avail:
			attack = get_req_attack_power(f,self.units,True)
			for i in self.myFactories:
				attack -= get_req_attack_power(i,self.units)
			if attack < 0:
				self.found_target = True
				self.targeted_factory = f
				return

	def converge(self):
		for f in self.myFactories:
			attack = get_req_attack_power(f,self.units)
			if attack > 0 and f != self.attack_point:
				self.commands.append('MOVE {} {} {}'.format(f[0],self.attack_point[0],attack))

	def FSM_run(self):
		# Next state
		self.state = self.next_state
		# Transition & behavior logic
		if self.state == State.conquer_free:
			self.commands.append('MSG s:conquer_free')
			# Conquer nearest useful factories
			for f in self.myFactories:
				nei = get_neighbour(f,self.factories)
				nei = get_avail(nei)
				nei = get_useful(nei)
				if len(nei) == 0: break
				for n in nei:
					if n in self.myFactories:
						break
					if n[2] < int(f[2]/2):
					    self.commands.append('MOVE {} {} {}'.format(f[0],n[0],int(f[2]/2)))

			if self.build_power > self.enemy_build_power or self.build_power > self.minimumBuildPower:
				self.next_state = State.build_army
			else:
				self.next_state = State.conquer_free

		elif self.state == State.build_army:
			self.commands.append('MSG s:build_army')
			# Defend factories
			self.defend()
			# Balance Units
			
			# Upgrade
			self.upgrade()
			# Conquer neutral adjacent factories
			self.conquer_adj()
			# Look for weak targets
			self.find_target()

			if self.found_target:
				self.next_state = State.prepare_attack
			else:
				self.next_state = State.build_army

		elif self.state == State.prepare_attack:
			self.commands.append('MSG s:prepare_attack on {}'.format(self.targeted_factory[0]))
			# Converge units on nearest factory
			if len(self.myFactories) == 0: return
			self.attack_point = get_neighbour(self.targeted_factory,self.myFactories)[0]
			self.converge()
			# Update info
			self.power_attack_factory = self.attack_point[2]
			self.power_target_factory = self.targeted_factory[2]*self.targeted_factory[3]*factory_dist[(self.attack_point[0],self.targeted_factory[0])]
			printf('{};{}'.format(self.power_attack_factory,self.power_target_factory))
			if self.targeted_factory in self.myFactories: return
			# If factory in danger
			for f in self.myFactories:
				if get_req_attack_power(f,self.units)<=0:
					self.next_state = State.build_army
			if not self.found_target:
				self.next_state = State.build_army
			elif self.power_attack_factory > self.power_factor*self.power_target_factory:
				self.next_state = State.attack
			else:
				self.next_state = State.prepare_attack


		elif self.state == State.attack:
			self.commands.append('MSG s:attack')
			self.found_target = False
			attack = get_req_attack_power(self.attack_point,self.units)
			self.commands.append('MOVE {} {} {}'.format(self.attack_point[0],self.targeted_factory[0],abs(attack)))
			self.targeted_factory = ()
			self.next_state = State.build_army

for i in range(link_count):
	factory_1, factory_2, distance = [int(j) for j in input().split()]
	factory_dist[(factory_1,factory_2)]=distance
	factory_dist[(factory_2,factory_1)]=distance
	factory_dist[(factory_2,factory_2)]=1e100
	factory_dist[(factory_1,factory_1)]=1e100

stalin = Conqueror()

# game loop
while True:
	entity_count = int(input())  # the number of entities (e.g. factories and troops)
	
	factories = []
	units = []
	bombs = []
	
	for i in range(entity_count):
		entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
		entity_id = int(entity_id)
		arg_1 = int(arg_1)
		arg_2 = int(arg_2)
		arg_3 = int(arg_3)
		arg_4 = int(arg_4)
		arg_5 = int(arg_5)
		if entity_type == "FACTORY":
			# [0]:id ; [1]:player ; [2]:units ; [3]:prod
			factories.append((entity_id,arg_1,arg_2,arg_3))
		elif entity_type == "TROOP":
			# [0]:id ; [1]:player ; [2]:fact.src ; [3]:fact.dst ; [4]:nb_units ; [5]:time
			units.append((entity_id,arg_1,arg_2,arg_3,arg_4,arg_5))
		elif entity_type == "BOMB":
			# [0]:id ; [1]:player ; [2]:fact.src ; [3]:fact.dst ; [4]:time ; [5]:-
			bombs.append((entity_id,arg_1,arg_2,arg_3,arg_4,arg_5))
	
	stalin.update_info((factories,units,bombs))