import sys, math

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
factory_dist = {}


def printf(s):
    print(s,file=sys.stderr)
    
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
    threshold = 5
    allUnits = get_units_count(fact,units)
    units_per_factories=[]
    for f in facts:
        unitFact = f[2]
        for u in units:
            if u[3] == f[0]:
                unitFact += u[4]
        units_per_factories.append(unitFact)
    for i in units_per_factories:
        if int(allUnits/len(fact))-threshold > i:
            ready = False
    return ready
    


for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    factory_dist[(factory_1,factory_2)]=distance
    factory_dist[(factory_2,factory_1)]=distance

# game loop
while True:
    entity_count = int(input())  # the number of entities (e.g. factories and troops)
    
    factories = []
    units = []
    
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
        elif entity_type == "TROOPS":
            # [0]:id ; [1]:player ; [2]:fact.src ; [3]:fact.dst ; [4]:nb_units ; [5]:time
            units.append((entity_id,arg_1,arg_2,arg_3,arg_4,arg_5))
    #print(get_enemy(factories), file=sys.stderr)
    myFactories = get_my(factories)
    availFactories = get_avail(factories)
    enemyFactories = get_enemy(factories)
    
    enemyUnits = get_enemy(units)
    myUnits = get_my(units)
    
    myFactInDanger = get_treat(myFactories,enemyUnits)
    
    orders = []
    # Conquer neutral factories
    if len(availFactories)!=0:
        for factory in myFactories:
        # Conquer nearest useful factories
            useful=get_useful(factories)
            useful=get_avail(useful)
            # Sort by distance
            useful.sort(key=lambda x: factory_dist[(factory[0],x[0])]) #printf(useful)
            targets=int(len(useful)/2)
            for i in range(targets):
                orders.append('MOVE {} {} {}'.format(factory[0],useful[i][0],useful[i][2]+2))
    elif len(myFactInDanger)!=0:
        orders.append('MSG Factory in danger')
        printf(myFactInDanger)
    else:
        #orders.append('MSG No danger')
        # Balance units
        printf('Balancing units')
        myFactoryCount = len(myFactories)
        totalUnits = get_units_count(myFactories,myUnits)
        unitThres = int(totalUnits/myFactoryCount)
        overPop = get_overpopulated(myFactories,myUnits,unitThres)
        underPop = get_underpopulated(myFactories,myUnits,unitThres)
        if len(overPop)!=0 and len(underPop)!=0:
            for f in overPop:
                underPopDist = get_distance_sorted(f,underPop)
                orders.append('MOVE {} {} {}'.format(f[0],underPopDist[0][0],f[2]-unitThres))


        if ready_to_attack(myFactories,myUnits):
            # Attack
            orders.append('MSG Ready to attack !')
            '''
            targetFactories = get_useful(enemyFactories)
            targetFactories = get_sorted_enemies(enemyFactories,enemyUnits)
            orders.append('Attacking factory {}'.format(targetFactories[0]))
            for f in myFactories:
'''
        
        
    # Print orders
    if len(orders)>1:
        print(';'.join(orders))
    elif len(orders)==1:
        print(orders[0])
    else:
        print('WAIT')