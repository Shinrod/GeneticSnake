# -*- coding: utf-8 -*-
'''
Neural Nework designed to copy a snake player
'''

### IMPORTS ###
import numpy as np
from math import e


### FUNCTIONS ###
def sigmoid(x):
    return 1/(1+e**(-float(x)))

def dsigmoid(y):
    #return sigmoid(x)*(1-sigmoid(x))
    return y*(1-y)


### MATRIX REPRODUCTION FUNCTIONS ###
def matrix_crossover(matrix_parent1,matrix_parent2,matrix_child):
    ''' Used in the crossover method '''
    nb_rows, nb_cols = np.shape(matrix_child)
    # Edit the DNA
    for i in range(nb_rows):
        for j in range(nb_cols):
            r = np.random.random()
            # There is half a chance for each weight to be given by the 1st parent
            if r <= 0.5:
                matrix_child[i][j] = matrix_parent1[i][j]
            # Else -> inherit from nn2
            else:
                matrix_child[i][j] = matrix_parent2[i][j]
    return matrix_child

def matrix_mutate(mutation_rate, matrix_child):
    ''' Used in mutate method '''
    nb_rows, nb_cols = np.shape(matrix_child)
    for i in range(nb_rows):
        for j in range(nb_cols):
            # Get a random number
            r = np.random.random()
            # See if a mutation occurs
            if r < mutation_rate :
                matrix_child[i][j] += np.random.normal()/5
                # Be sure the weight stays between -1 and 1
                if matrix_child[i][j] > 1 :
                    matrix_child[i][j] = 1
                elif matrix_child[i][j] < -1:
                    matrix_child[i][j] = -1
    return matrix_child


### CLASS ###
class NeuralNetwork:
    
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        ''' Build a 3 layers neural network '''
        self.input_nodes    = input_nodes
        self.hidden_nodes   = hidden_nodes
        self.output_nodes   = output_nodes
        self.weight_ih      = np.random.rand(hidden_nodes,input_nodes)*2-1
        self.weight_ho      = np.random.rand(output_nodes,hidden_nodes)*2-1
        self.bias_h         = np.random.rand(hidden_nodes,1)*2-1
        self.bias_o         = np.random.rand(output_nodes,1)*2-1
        
    def feedforward(self,inputs):
        ''' Basically use the brain '''
        inputs = np.array(inputs)
        inputs.resize((len(inputs),1))
        # Get the hidden neurons values
        hidden = np.dot(self.weight_ih, inputs)
        hidden += self.bias_h
        hidden = np.array(list(np.vectorize(sigmoid)(hidden)))
        # Get the output value
        outputs = np.dot(self.weight_ho, hidden)
        outputs += self.bias_o
        outputs = np.array(list(np.vectorize(sigmoid)(outputs)))
        outputs = outputs.flatten()
        return list(outputs)
        
    ### GENETIC THING ###
    def crossover(self,parent2):
        ''' GENETIC : Make a child based on 2 parents '''
        child = NeuralNetwork(24,10,4)
        # Crossover the weight_ih
        child.weight_ih = matrix_crossover(self.weight_ih, parent2.weight_ih, child.weight_ih)
        # Crossover the weight_ho
        child.weight_ho = matrix_crossover(self.weight_ho, parent2.weight_ho, child.weight_ho)
        # Crossover the bias_h1
        child.bias_h = matrix_crossover(self.bias_h, parent2.bias_h, child.bias_h)
        # Crossover the bias_o
        child.bias_o = matrix_crossover(self.bias_o, parent2.bias_o, child.bias_o)
        return child    
    
    def mutate(self, mutation_rate):
        ''' GENETIC : Have some mutaions based on the mutation rate '''
        # Mutate the weight_ih
        self.weight_ih = matrix_mutate(mutation_rate, self.weight_ih)
        # Mutate the weight_ho
        self.weight_ho = matrix_mutate(mutation_rate,self.weight_ho)
        # Mutate the bias_h
        self.bias_h = matrix_mutate(mutation_rate,self.bias_h)
        # Mutate the bias_o
        self.bias_o = matrix_mutate(mutation_rate,self.bias_o)