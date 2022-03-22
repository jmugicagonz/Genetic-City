
# -*- coding: utf-8 -*-

"""
 ██████╗ ███████╗███╗   ██╗███████╗████████╗██╗ ██████╗     ██████╗██╗████████╗██╗   ██╗
██╔════╝ ██╔════╝████╗  ██║██╔════╝╚══██╔══╝██║██╔════╝    ██╔════╝██║╚══██╔══╝╚██╗ ██╔╝
██║  ███╗█████╗  ██╔██╗ ██║█████╗     ██║   ██║██║         ██║     ██║   ██║    ╚████╔╝
██║   ██║██╔══╝  ██║╚██╗██║██╔══╝     ██║   ██║██║         ██║     ██║   ██║     ╚██╔╝
╚██████╔╝███████╗██║ ╚████║███████╗   ██║   ██║╚██████╗    ╚██████╗██║   ██║      ██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝     ╚═════╝╚═╝   ╚═╝      ╚═╝

DESCRIPTION: TBD

By: Juan Mugica - jmugicag@mit.edu
MIT Media Lab - City Science Group

"""
#TODO: REMOVE COMMENTED UNNECESSARY CODE 

import numpy as np                                                              #Matrix and array handling.
import matplotlib.pyplot as plt                                                 #Plotting

from blockgenerationfunctions import *                                          #Functions for creating new city arrays.
from fitnessFunctions import *                                                  #Functions for evaluation fitness of cities.
from crossfunctions import *                                                    #Functions for crossing individuals.
from mutation_functions import *                                                #Functions for mutating individuals.
from selectionFunctions import *                                                #Functions for best individual selection.
from plotting import *                                                          #Functions for plotting
from parameters import *
from connections import *                                                       #Import functions for including roads
from initFunctions import *                                                     #Import initial calculations
import ray

#Placeholder variables
population_matrix = np.arange(block_size * block_size) # Matrix for storing populations within process.
selected_matrix = np.zeros((population_size, block_size*block_size)) # Matrix for selected populations within process.
gen = np.arange(num_generations) + 1
final_blocks = np.zeros((block_size,block_size)) # Matrix for storing the best blocks coming from the last iteration
so_far_blocks = np.zeros((block_size,block_size)) # Matrix for storing the best blocks coming from some iterations and see the progress

#TODO: make it support multiple columns
best_outputs = []

#Create list to store fitness for different rules
fitness_rules_solutions = []

# Starting Ray for parallelization
ray.init()

# Create New Population #################################
#print('NEW POPULATION!')
population_matrix = create_population(population_size, block_size, building_types) #Creates new block.
print("Initial population")
print(population_matrix)
#START OF GENERATON LOOP ################################################################################################################
for generation in range(0, num_generations):
    print("Generation : ", generation)

    fitness_vector, list_of_dictionaries_rules = evaluate_blocks(population_matrix, dictionary_rules)
    best_match_idx = np.where(fitness_vector == np.max(fitness_vector))
    best_value = np.max(fitness_vector)
    best_outputs.append(best_value)

    # Selecting the best parents in the population for mating.
    parents = select_mating_pool(fitness_vector, population_matrix, num_parents_mating)

    #Cross
    offspring_crossover = crossover(parents,offspring_size=(population_size-parents.shape[0], block_size*block_size),crossover_value=crossover_value)

    # Adding some variations to the offspring using mutation.
    offspring_mutation = mutation(offspring_crossover, prob_mutation, block_size, building_types)

    # Creating the new population based on the parents and offspring.
    population_matrix[0:parents.shape[0], :] = parents
    population_matrix[parents.shape[0]:, :] = offspring_mutation


# Getting the best solution after iterating finishing all generations.
#At first, the fitness is calculated for each solution in the final generation.
fitness_vector, list_of_dictionaries_rules = evaluate_blocks(population_matrix, dictionary_rules) # Then return the index of that solution corresponding to the best fitness.
best_match_idx = np.where(fitness_vector == np.max(fitness_vector))

