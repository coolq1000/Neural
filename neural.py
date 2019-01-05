from copy import deepcopy
import random

class Neuron:

    def __init__(self, value=0, bias=0):
        self.value = value
        self.weights = []
        self.bias = bias

class Network:

    def __init__(self, topology):
        # Initialize layers,
        self.layers = [[Neuron() for x in range(y)] for y in topology]

        # Initialize weights,
        for l, layer in enumerate(self.layers):
            for neuron in layer:
                if l != len(self.layers) - 1:
                    nl = len(self.layers[l + 1])
                    neuron.weights += [0] * nl
    
    def forward_propagate(self):
        """ Iterate through each layer """
        for l in range(1, len(self.layers)):
            """ Iterate through each neuron in each layer """
            for n in range(len(self.layers[l])):
                total = 0
                for pn in range(len(self.layers[l - 1])):
                    total += (self.layers[l - 1][pn].value + self.layers[l][n].bias) * self.layers[l - 1][pn].weights[n]
                self.layers[l][n].value = total
    
    def mutate(self, ratio):
        """ Iterate through each layer """
        for l in range(len(self.layers)):
            """ Iterate through each neuron in each layer """
            for n in range(len(self.layers[l])):
                self.layers[l][n].bias += (1 - random.random() * 2) * ratio
                for w in range(len(self.layers[l][n].weights)):
                    self.layers[l][n].weights[w] += (1 - random.random() * 2) * ratio
    
    def get_outputs(self):
        return [x.value for x in self.layers[-1]]

    def set_inputs(self, vals):
        for i, val in enumerate(vals):
            self.layers[0][i].value = val

    def show(self):
        for layer in self.layers:
            for neuron in layer:
                print(neuron.value, end='')
            print()

class Generation:

    def __init__(self, topology, size, mutation_rate=0.1):
        self.mutation_rate = mutation_rate
        self.networks = [Network(topology) for x in range(size)]
        self.fitness  = [0] * size
        self.pointer  = 0

    def set_fit(self, val):
        self.fitness[self.pointer] = val
    
    def add_fit(self, val):
        self.fitness[self.pointer] += val
    
    def set_inputs(self, vals):
        for i, val in enumerate(vals):
            self.networks[self.pointer].layers[0][i].value = int(val)

    def forward_propagate(self):
        self.networks[self.pointer].forward_propagate()

    def get_outputs(self):
        return [x.value for x in self.networks[self.pointer].layers[-1]]

    def switch(self):
        self.pointer += 1
        if self.pointer >= len(self.networks):
            self.pointer = 0
            self.next_gen()
    
    def next_gen(self):
        champion = deepcopy(self.networks[self.fitness.index(max(self.fitness))])
        for nn in range(len(self.networks)):
            self.networks[nn] = deepcopy(champion)
            self.fitness[nn] = 0
            if nn != 0:
                self.networks[nn].mutate(self.mutation_rate)
