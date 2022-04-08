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
from progressbar import printProgressBar #Import progress bar function.
from parameters import *
from rules import *
import ray


#Local task
def fitness_func(solution, set_rules, weights):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    #Create dictionary for storing fitness functions
    dictionary_rules_fitness = {str(rule.__name__):0 for rule in set_rules}
    fitness=0.0
    counterWeights = 0
    unique, counts = np.unique(solution,return_index=False, return_inverse=False, return_counts=True, axis=None)
    lists_of_distances = []
    lists_of_distances = dist_h_o_p(solution)
    if (counts.size < 3): return 0 #If there are no parks, or offices, or residences, don't consider the solution.
    for index, rule in enumerate(set_rules):
        fitness_value = rule(solution,unique,counts,lists_of_distances)
        fitness += weights[str(rule.__name__)]*fitness_value
        dictionary_rules_fitness[str(rule.__name__)] = fitness_value/100
        #We need these calculations to normalize the fitness function and put it between 0 and 1. TODO: maybe in the future it will be itneresting to make it depend on "available features and not those != 0"
        if(weights[str(rule.__name__)] != 0): counterWeights += weights[str(rule.__name__)]
        elif(fitness_value != 0): counterWeights += 1
    #Then we return a fitness function between 0 and 100
    fitness = fitness / (counterWeights)
    return fitness, dictionary_rules_fitness

# Ray task
remote_fitness_func = ray.remote(fitness_func)

def evaluate_blocks(block_to_ev, set_rules, weights): #Complete evaluation function for looping through every individual of a population.
    population_size=block_to_ev.shape[0]
    ev_vector = np.zeros(population_size)
    list_of_dictionaries_rules = []*population_size
    ray_object = ray.get([remote_fitness_func.remote(block_to_ev[pop,:], set_rules, weights) for pop in range(population_size)])
    ev_vector = [i[0] for i in ray_object]
    list_of_dictionaries_rules = [i[1] for i in ray_object]
    #printProgressBar(population_size, population_size, prefix = 'Population Evaluation Progress:', suffix = 'Complete', length = 50)
    return ev_vector, list_of_dictionaries_rules #Returns evaluation vector.