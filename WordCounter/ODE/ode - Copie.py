import random
import numpy as np
import matplotlib.pyplot as plt
       
class Filter:
    def __init__(self, b, a):
        self.b = b
        self.p = [0 for x in b]
        self.a = a
        self.q = [0 for x in a]
        self.out = 0

    def input(self, x):
        # Insert the signal
        self.p.insert(0, x)
        self.p.pop(len(self.p)-1)

        # Compute output
        y1 = np.dot(self.b,self.p)

        self.out = self.a[0] * (np.dot(self.a[1:],self.q[1:]) + y1)
        self.q.insert(0, self.out)
        self.q.pop(len(self.q)-1)
        return self.out


def f_dirac(i):
    if i==0:
        return 1
    else:
        return 0

def f_step(i):
    if i >= 0:
        return 1
    else:
        return 0

def impulse_rep(b, a, minX, maxX):
    # Build signal
    h = Filter(b,a)
    xPlt = range(minX, maxX)
    xIn = [f_dirac(x)for x in xPlt]
    y = [h.input(x) for x in xIn]
    
    # Plot imput
    plt.plot(xPlt, xIn, 'x')
    plt.stem(xPlt, y, 'r')
    plt.show()

def step_rep(b, a, minX, maxX):
    # Build signal
    h = Filter(b,a)
    xPlt = range(minX, maxX)
    xIn = [f_step(x)for x in xPlt]
    y = [h.input(x) for x in xIn]
    
    # Plot imput
    plt.plot(xPlt, xIn, 'o')
    plt.stem(xPlt, y, 'r')
    plt.show()

impulse_rep([1,1],[1,0],-10,10)
#step_rep([1,0],[1,0.5],-10,30)
R=10
L=0.001
C=0.000002
#impulse_rep([1,0],[1,1/(L*C),R/L],-10,10)
