import random
import numpy as np
import matplotlib.pyplot as plt
       
class Filter:
    def __init__(self, b):
        self.b = b
        self.p = [0 for x in b]
        self.out = 0

    def input(self, x):
        # Insert the signal
        self.p.insert(0, x)
        self.p.pop(len(self.p)-1)

        # Compute output
        self.out = np.dot(self.b,self.p)
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

def impulse_rep(b, minX, maxX):
    # Build signal
    h = Filter(b)
    xPlt = range(minX, maxX)
    xIn = [f_dirac(x)for x in xPlt]
    y = [h.input(x) for x in xIn]
    
    # Plot imput
    plt.plot(xPlt, xIn, 'o')
    plt.stem(xPlt, y, 'r')
    plt.show()

def step_rep(b, minX, maxX):
    # Build signal
    h = Filter(b)
    xPlt = range(minX, maxX)
    xIn = [f_step(x)for x in xPlt]
    y = [h.input(x) for x in xIn]
    
    # Plot imput
    plt.plot(xPlt, xIn, 'o')
    plt.stem(xPlt, y, 'r')
    plt.show()

impulse_rep([1,2,4,5],-10,10)
step_rep([1,2,4,5],-10,10)
