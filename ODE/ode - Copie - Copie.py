import random
import numpy as np
import matplotlib.pyplot as plt
       
class Filter:
    def __init__(self, b, a):
        self.b = b
        self.p = [0 for x in range(len(b))]
        self.a = [-x for x in a]
        self.out = 0

    def input(self, x):
        # Compute q1
        q1 = x + np.dot(self.p[1:],self.a[1:])
        
        # Compute output
        y = q1*self.b[0] + np.dot(self.p[1:],self.b[1:])
        self.out = y

        # Shift buffer
        self.p.insert(1, x)
        self.p.pop(len(self.p)-1)
        
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
    plt.figure(1)
    plt.subplot(211)
    plt.title("Impulse response")
    plt.stem(xPlt, xIn, 'r')
    plt.subplot(212)
    plt.stem(xPlt, y, 'r')
    plt.show()

def step_rep(b, a, minX, maxX):
    # Build signal
    h = Filter(b,a)
    xPlt = range(minX, maxX)
    xIn = [f_step(x)for x in xPlt]
    y = [h.input(x) for x in xIn]
    
    # Plot imput
    plt.figure(2)
    plt.subplot(211)
    plt.title("Step response")
    plt.stem(xPlt, xIn, 'r')
    plt.subplot(212)
    plt.stem(xPlt, y, 'r')
    plt.show()

minVal = -10
maxVal = 30
a_f = [1,0.1,0.1]
b_f = [0,2,3]
impulse_rep(b_f,a_f,minVal,maxVal)
step_rep(b_f,a_f,minVal,maxVal)
R=10
L=0.001
C=0.000002

