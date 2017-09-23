import random
import numpy as np

# sigmoid function
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

class Neuron:
    weight = []
    output = 0.0
    bias = False

    def __init__(self, inNbr, isBias):
        self.weight = []
        if isBias == False:
            # Initiate weights with random values
            for x in range(inNbr):
                print(x)
                self.weight.append(random.random())
        else:
            self.bias = True
            self.output = 1.0
        
class NeuralNetwork:
    topology = []
    inputVector = []
    outputVector = []
    network = []

    def __init__(self, topo):
        self.topology = topo

        # Create weight vector
        wV = [len(self.inputVector)]
        for x in self.topology[:-1]:
            wV.append(x)
        #print(wV)
        
        # Create network
        for layerSize,layerI,w in zip(self.topology,range(len(self.topology)),wV):
            layer = []
            print(w)
            # Create layer
            for n in range(layerSize):
                layer.append(Neuron(w,False))
            # Bias neuron
            layer.append(Neuron(0,True))
            # Add to network
            self.network.append(layer)

    def getOutput(self):
        out = []
        for neuron in self.network[len(network)-1]:
            out.append(neuron.output)
        return out

    def feedForward(self,inp):
        lastLayer = inp
        for layer in self.network:
            for neuron in layer[:-1]:
                neuron.output = nonlin(np.dot(lastLayer,neuron.weight),False)
            # Update lastLayer
            lastLayer = []
            for neuron in layer:
                lastLayer.append(neuron.output)

neuralNet = NeuralNetwork([5,4,3,2])
