import sys
import math

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
world=Graph(factory_count)
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]

# game loop
while True:
    entity_count = int(input())  # the number of entities (e.g. factories and troops)
    myFactories = []
    availFactories = []
    enemyFactories = []
    factoryProd = []
    factoryUnits = []
    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)
        #print("F:{},prod:{}".format(arg_1,arg_3), file=sys.stderr)
        if entity_type == "FACTORY":
            if arg_1 == 1: myFactories.append((entity_id,arg_3))
            elif arg_1 == 0: availFactories.append(entity_id)
            elif arg_1 == -1: enemyFactories.append((entity_id,arg_2))
            factoryProd.append((entity_id, arg_3,arg_1))
            factoryUnits.append((entity_id, arg_2))
    print(factoryProd, file=sys.stderr)
    print(factoryUnits, file=sys.stderr)
    
    # Take available factories
    if len(availFactories)!=0:
        fact=factoryProd
        fact.sort(key=lambda x : x[1],reverse=True)
        myFactories.sort(key=lambda x : x[1],reverse=True)
        while fact[0][0] == myFactories[0][0] or abs(fact[0][2])==1: fact.pop(0)
        print(fact, file=sys.stderr)
        print('MOVE {} {} {}'.format(myFactories[0][0],fact[0][0],2))
        
    # Conquest
    else:
        fact=enemyFactories
        fact.sort(key=lambda x : x[1],reverse=False)
        myFactories.sort(key=lambda x : x[1],reverse=True)
        print('MOVE {} {} {}'.format(myFactories[0][0],fact[0][0],2))

