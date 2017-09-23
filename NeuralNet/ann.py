import random

class Neuron:
    weight = []
    output = 0.0
    bias = False

    def __init__(self, inNbr, isBias):
        if isBias == False:
            # Initiate weights with random values
            for x in range(inNbr):
                self.weight.append(random.random())
        else:
            self.bias = True
            self.output = 1.0
        
class NeuralNetwork:
    topology = []
    inputVector = []
    outputVector = []
    network = {}

    def __init__(self, topo):
        self.topology = topo

        # Create weight vector
        wV = [len(self.inputVector)]
        for x in self.topology[:-1]:
            wV.append(x)
        
        # Create network
        for layerSize,layerI,w in zip(self.topology,range(len(self.topology)),wV):
            # Create layer
            for n in range(layerSize):
                self.network[layerI,n] = Neuron(w,False)
            # Bias neuron
            self.network[layerI,layerSize] = Neuron(0,True)
            
