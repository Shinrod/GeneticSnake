# -*- coding: utf-8 -*-
''' Generation Class for NeuroEvolution '''

### IMPORTS ###
from ClassNeuralNet import NeuralNetwork
import numpy as np


### CLASS ###
class Generation:
    
    ## CONSTRUCTOR ###
    def __init__(self, demography, fitFunction, inputs = 24, hidden = 10, output = 4, loading = False):
        ''' Set up the generation & parameters '''
        # Get thoose params if the Generation isn't loaded from a file
        self.demography = demography
        # Params for the NeuralNet
        self.inputs = inputs
        self.hidden = hidden
        self.output = output
        self.population = [NeuralNetwork(self.inputs, self.hidden, self.output) for i in range(self.demography)]
        # Mutation rate
        self.mr = 0.1
        # Fitness function
        self.fitFunction = fitFunction
        self.num_gen = 1
        self.getScores()
    
    ## METHODS ##                
    def step(self):
        '''
        Make 1 step of genetic thing
        '''
        self.naturalselection()
        self.getScores()
        self.num_gen += 1
        
        
    def getScores(self):
        ''' Get the scores '''
        self.score = self.evaluate()
        self.total_score = self.get_total_score()
        self.best = self.get_best()
        
        
    def evaluate(self):
        '''
        Return an array with the list of the fitness scores
        <fitFunction> must return the fitness value of the Network
        '''
        score = []
        current_best = 0
        # Get a Neural Net
        for i, nn in enumerate(self.population):
            score.append(self.fitFunction(nn))
            # Print the new score if it's better than the previous one
            if score[-1] > current_best:
                current_best = score[-1]
                print('Net :', i)
                print('Score :', current_best)
                print()
        return score
    
    def get_best(self):
        ''' Return the best Net of the population '''
        score_max = max(self.score)
        index_max = self.score.index(score_max)
        return self.population[index_max]
    
    
    def get_total_score(self):
        ''' Calculate it once so it won't calculate it each time it needs it '''
        total_score = 0
        for score in self.score:
            total_score += score
        return total_score
        
    
    def pickOne(self):
        ''' Pick a random brain of the population based on the score '''
        # Normalise the scores to have a prob
        self.score = np.array(self.score)
        self.prob = self.score / self.total_score
        self.score = list(self.score)
        # Pick a random number
        r = np.random.rand()
        for i in range(len(self.population)):
            r = r - self.prob[i]
            if r <= 0 :
                return self.population[i]
    
    
    def naturalselection(self):
        ''' Make a new generation '''
        # Save the best of the last population
        new_pop = [self.best]
        # Make the new genertion
        for i in range(1,self.demography):
            # Pick 2 parents for the crossover
            parent1 = self.pickOne()
            parent2 = self.pickOne()
            child = parent1.crossover(parent2)
            # Mutate the child (based on the mutation rate)
            child.mutate(self.mr)
            new_pop.append(child)
        self.population = new_pop
