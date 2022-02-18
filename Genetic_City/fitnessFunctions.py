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



# Matrix with the block size and where each element is equal to the tuple that gives its position
def block_matrix(grid_size):
    reshaped = np.reshape([[i,j] for i in range(grid_size) for j in range(grid_size)],(grid_size,grid_size,1,2))
    return [[i,j] for i in range(grid_size) for j in range(grid_size)]

# Matrix containing the manhattan distance between two indexes
def manhattan_table(block_matrix):
    return scipy.spatial.distance_matrix(block_matrix,block_matrix,p=1)


def fitness_func(solution, distance_table):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    
    #printProgressBar(0, population, prefix = 'Population Evaluation Progress:', suffix = 'Complete', length = 50)
    
    #The fitness function will return a greater value if number of parks increases. Should converge into more parks.
    unique, counts = np.unique(solution,return_index=False, return_inverse=False, return_counts=True, axis=None)
    #COMPUTE FITNESS OF PARKS BALANCE
    #fitness = green_space_balance_amount(counts[0],np.shape(solution)[0],percentage_of_parks)
    fitness = int(1000*green_space_balance_width(solution,distance_table)+
            green_space_balance_amount(counts[0],np.shape(solution)[0],percentage_of_parks))
    return fitness

def evaluate_blocks(block_to_ev, distance_table): #Complete evaluation function for looping through every individual of a population.
    population_size=block_to_ev.shape[0]
    printProgressBar(0, population_size, prefix = 'Population Evaluation Progress:', suffix = 'Complete', length = 50)
    ev_vector = np.arange(population_size)
    for pop in range(0, population_size):
        ev_vector[pop] = fitness_func(block_to_ev[pop,:], distance_table) #Change line to change to desired weight function.
        printProgressBar(pop + 1, population_size, prefix = 'Population Evaluation Progress:', suffix = 'Complete', length = 50)
    return ev_vector #Returns evaluation vector.


















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