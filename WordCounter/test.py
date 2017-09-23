import sys
import math

def bfs(ad,s):
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
    
    print('Parent graph: {}'.format(parent))
    print('Weight graph: {}'.format(level))
    return parent,level

# Dict of all adjacent nodes
adj = {0: [1], 1: [0, 2], 2: [1, 3, 4], 3: [2], 4: [2]}

print(adj)

bfs(adj,0)

