import sys
import math

############ Dijkstra algo ##################
import queue  
from collections import namedtuple

Edge = namedtuple('Edge', ['vertex', 'weight'])


class Graph(object):  
    def __init__(self, vertex_count):
        self.vertex_count = vertex_count
        self.adjacency_list = [[] for _ in range(vertex_count)]

    def add_edge(self, source, dest, weight):
        assert source < self.vertex_count
        assert dest < self.vertex_count
        self.adjacency_list[source].append(Edge(dest, weight))
        self.adjacency_list[dest].append(Edge(source, weight))

    def get_edge(self, vertex):
        for e in self.adjacency_list[vertex]:
            yield e

    def get_vertex(self):
        for v in range(self.vertex_count):
            yield v


def dijkstra(graph, source, dest):  
    q = queue.PriorityQueue()
    parents = []
    distances = []
    start_weight = float("inf")

    for i in graph.get_vertex():
        weight = start_weight
        if source == i:
            weight = 0
        distances.append(weight)
        parents.append(None)

    q.put(([0, source]))

    while not q.empty():
        v_tuple = q.get()
        v = v_tuple[1]

        for e in graph.get_edge(v):
            candidate_distance = distances[v] + e.weight
            if distances[e.vertex] > candidate_distance:
                distances[e.vertex] = candidate_distance
                parents[e.vertex] = v
                # primitive but effective negative cycle detection
                if candidate_distance < -1000:
                    raise Exception("Negative cycle detected")
                q.put(([distances[e.vertex], e.vertex]))

    shortest_path = []
    end = dest
    while end is not None:
        shortest_path.append(end)
        end = parents[end]

    shortest_path.reverse()

    return shortest_path, distances[dest]
##########################################

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
world=Graph(factory_count)
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    world.add_edge(factory_1, factory_2, distance)

#print(dijkstra(world, 0,factory_count-1), file=sys.stderr)

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
            elif arg_1 == -1: enemyFactories.append(entity_id)
            factoryProd.append((entity_id, arg_3))
            factoryUnits.append((entity_id, arg_2))
    print(factoryProd, file=sys.stderr)
    print(factoryUnits, file=sys.stderr)
    
    # Take available factories
    if len(availFactories)!=0:
        factoryProd.sort(key=lambda x : x[1],reverse=True)
        myFactories.sort(key=lambda x : x[1],reverse=True)
        print(factoryProd, file=sys.stderr)
        print('MOVE {} {} {}'.format(myFactories[0][0],factoryProd[0][0],2))
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
    print("WAIT")
