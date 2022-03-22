# -*- coding: utf-8 -*-

"""
 ██████╗ ███████╗███╗   ██╗███████╗████████╗██╗ ██████╗     ██████╗██╗████████╗██╗   ██╗
██╔════╝ ██╔════╝████╗  ██║██╔════╝╚══██╔══╝██║██╔════╝    ██╔════╝██║╚══██╔══╝╚██╗ ██╔╝
██║  ███╗█████╗  ██╔██╗ ██║█████╗     ██║   ██║██║         ██║     ██║   ██║    ╚████╔╝
██║   ██║██╔══╝  ██║╚██╗██║██╔══╝     ██║   ██║██║         ██║     ██║   ██║     ╚██╔╝
╚██████╔╝███████╗██║ ╚████║███████╗   ██║   ██║╚██████╗    ╚██████╗██║   ██║      ██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝     ╚═════╝╚═╝   ╚═╝      ╚═╝

Functions used for evaluation of city populations for algorithm.

By: Juan Mugica - jmugicag@mit.edu
MIT Media Lab - City Science Group
                                                                                      """

from tracemalloc import stop
from matplotlib.pyplot import grid
import numpy as np
import scipy.spatial
from parameters import *
from rules import *
from progressbar import printProgressBar #Import progress bar function.
import time
import ray


# Ray task
@ray.remote
def fitness_func(solution, dictionary_rules):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    #Create dictionary for storing fitness functions
    dictionary_rules_fitness = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}
    fitness=0.0
    counterWeights = 0
    unique, counts = np.unique(solution,return_index=False, return_inverse=False, return_counts=True, axis=None)
    lists_of_distances = []
    lists_of_distances = distances_homes_offices_parks(solution)
    if (counts.size < 3): return 0 #If there are no parks, or offices, or residences, don't consider the solution.
    for key in dictionary_rules:
        fitness_value = dictionary_rules[key](solution,unique,counts,lists_of_distances)
        fitness += weights[key]*fitness_value
        dictionary_rules_fitness[key] = fitness_value
        #We need these calculations to normalize the fitness function and put it between 0 and 100. TODO: maybe in the future it will be itneresting to make it depend on "available features and not those != 0"
        if(weights[key] != 0): counterWeights += weights[key]
        elif(fitness_value != 0): counterWeights += 1
    #Then we return a fitness function between 0 and 100
    fitness = fitness / (counterWeights)
    return fitness, dictionary_rules_fitness

def evaluate_blocks(block_to_ev, dictionary_rules): #Complete evaluation function for looping through every individual of a population.
    population_size=block_to_ev.shape[0]
    ev_vector = np.zeros(population_size)
    list_of_dictionaries_rules = []*population_size
    ray_object = ray.get([fitness_func.remote(block_to_ev[pop,:], dictionary_rules) for pop in range(population_size)])
    ev_vector = [i[0] for i in ray_object]
    list_of_dictionaries_rules = [i[1] for i in ray_object]
    printProgressBar(population_size, population_size, prefix = 'Population Evaluation Progress:', suffix = 'Complete', length = 50)
    return ev_vector, list_of_dictionaries_rules #Returns evaluation vector.