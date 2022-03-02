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
    printProgressBar(0, population_size, prefix = 'Population Evaluation Progress:', suffix = 'Complete', length = 50)
    ev_vector = np.zeros(population_size)
    list_of_dictionaries_rules = []
    for pop in range(0, population_size):
        ev_vector[pop],dictionary_rules_fitness = fitness_func(block_to_ev[pop,:], dictionary_rules) #Change line to change to desired weight function.
        list_of_dictionaries_rules.append(dictionary_rules_fitness)
        printProgressBar(pop + 1, population_size, prefix = 'Population Evaluation Progress:', suffix = 'Complete', length = 50)
    return ev_vector, list_of_dictionaries_rules #Returns evaluation vector.


















'''


def evaluate_balanced(evcity):
    total_evaluation = 0
    wheights = np.array([0, 0, 0, 0, 0, 10, 10, 10, 10]) #Weights used by function to evaluate. Places more interest in high numbers.
    unique, counts = np.unique(evcity,return_index=False, return_inverse=False, return_counts=True, axis=None)
    dictionary = dict(zip(unique, counts))
    for type in range(1,10):
        #print(dictionary[1])
        if type in evcity:
            total_evaluation = total_evaluation + (dictionary[type] * wheights[type - 1]) #Objective fucntion. This function will change as real city metrics are added to algorithm.
    return total_evaluation

def evaluate_simplethree(evcity, look_up):
    unique, counts = np.unique(evcity,return_index=False, return_inverse=False, return_counts=True, axis=None)
    if counts.size < 3:
        evaluation = 0

    #Set minimun quantities for amenities
    elif counts[0] < 3 or counts[1] < 4 or counts[2] < 4:
        evaluation = 0

    else:
        evaluation = 1000
        homes = np.where(evcity == 3)
        offices = np.where(evcity == 1)
        parks = np.where(evcity == 2)

        for home in range(int(homes[0].shape[0])):
            for office in range(offices[0].shape[0]):
                evaluation = evaluation - look_up[homes[0][home], offices[0][office]]
            for park in range(parks[0].shape[0]):
                evaluation = evaluation - look_up[homes[0][home], parks[0][park]]

        for park in range(int(parks[0].shape[0])):
            for office in range(offices[0].shape[0]):
                evaluation = evaluation - look_up[parks[0][park], offices[0][office]]


    return evaluation

"""
else:
    evaluation = 1000 - abs(counts[0]- counts[1]) - abs(counts[0]- counts[2]) - abs(counts[1]- counts[2])
"""

def evaluate_cities(city_to_ev, population, look_up ): #Complete evaluation function for looping through every individual of a population.
    printProgressBar(0, population, prefix = 'Population Evaluation Progress:', suffix = 'Complete', length = 50)
    ev_vector = np.arange(population)
    for pop in range(0, population):
        ev_vector[pop] = evaluate_simplethree(city_to_ev[pop,:], look_up) #Change line to change to desired weight function.
        printProgressBar(pop + 1, population, prefix = 'Population Evaluation Progress:', suffix = 'Complete', length = 50)
    return ev_vector #Returns evaluation vector.
'''