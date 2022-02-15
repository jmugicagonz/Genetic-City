
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

#from turtle import distance
import numpy as np                                                              #Matrix and array handling.
import matplotlib.pyplot as plt                                                 #Plotting
import pygad as ga

#from numpy import empty
from blockgenerationfunctions import *                                          #Functions for creating new city arrays.
from fitnessFunctions import *                                                  #Functions for evaluation fitness of cities.
#from progressbar import printProgressBar                                       #Helps with progress bar in terminal.
from crossfunctions import *                                                    #Functions for crossing individuals.
from mutation_functions import *                                                #Functions for mutating individuals.
from selectionFunctions import *                                                #Functions for best individual selection.
from plotting import *                                                          #Functions for plotting
from parameters import *


#Placeholder variables
population_matrix = np.arange(block_size * block_size) # Matrix for storing populations within process.
#evaluation_vector = np.arange(population_size) #Evaluation vector used for selection.
selected_matrix = np.zeros((population_size, block_size*block_size)) # Matrix for selectec populations within process.
#crossed_population_matrix = np.zeros((population_size, block_size*block_size)) # Matrix for storing crossed populations within process.
#mutated_population_matrix = np.zeros((population_size, block_size*block_size)) # Matrix for storing mutated populations within process.
#best_found_ev = np.zeros(num_generations) # Matrix for storing the best found evaluation
gen = np.arange(num_generations) + 1
#best_found_indiv = np.zeros(block_size * block_size)
#last_fitness = -1e10 #Saves best solution fitness value

final_blocks = np.zeros((block_size*city_size,block_size*city_size )) # Matrix for storing the best blocks coming from the last iteration


distance_table  = manhattan_table(block_matrix(block_size))

#TODO: make it support multiple columns
best_outputs = []
for column_blocks in range(city_size):

    for row_blocks in range(city_size):
        print('THIS IS BLOCK #:', row_blocks)

        # Create New Population #################################
        #print('NEW POPULATION!')
        population_matrix = create_population(population_size, block_size, building_types) #Creates new block.
        print("Initial population")
        print(population_matrix)
        #START OF GENERATON LOOP ################################################################################################################
        printProgressBar(0, population_size, prefix = 'Generation Progress:', suffix = 'Complete', length = 50)
        for generation in range(0, num_generations):
            print("Generation : ", generation)

            fitness_vector = evaluate_blocks(population_matrix, population_size, distance_table)
            #print("Fitness")
            #print(fitness_vector)

            best_value = np.max(fitness_vector)
            best_outputs.append(best_value)
            # The best result in the current iteration.
            #print("Best result : ", best_value)


            # Selecting the best parents in the population for mating.
            parents = select_mating_pool(fitness_vector, population_matrix, num_parents_mating)

            #print("Parents")
            #print(parents)

            #Cross
            offspring_crossover = crossover(parents,offspring_size=(population_size-parents.shape[0], block_size*block_size),crossover_value=crossover_value)

            #print("Crossover")
            #print(offspring_crossover)


            # Adding some variations to the offspring using mutation.
            offspring_mutation = mutation(offspring_crossover, prob_mutation, block_size, building_types)
            #print("Mutation")
            #print(offspring_mutation)

            # Creating the new population based on the parents and offspring.
            population_matrix[0:parents.shape[0], :] = parents
            population_matrix[parents.shape[0]:, :] = offspring_mutation
            #print("Population after generation")
            #print(population_matrix)

        # Getting the best solution after iterating finishing all generations.
        #At first, the fitness is calculated for each solution in the final generation.
        fitness_vector = evaluate_blocks(population_matrix, population_size, distance_table) # Then return the index of that solution corresponding to the best fitness.
        best_match_idx = np.where(fitness_vector == np.max(fitness_vector))

        print("Best solution : ", population_matrix[best_match_idx, :])
        print("Best solution fitness : ", fitness_vector[best_match_idx])
        print("Best match index: ",best_match_idx)


        '''plt.plot(best_outputs)
        plt.xlabel("Iteration")
        plt.ylabel("Fitness")
        plt.show()'''
        final_blocks[row_blocks*block_size:(row_blocks*block_size)+block_size, column_blocks*block_size:(column_blocks*block_size)+block_size] = np.reshape(population_matrix[best_match_idx[0].shape[0], :], (block_size, block_size))
        if visualizations: np.savetxt('C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City/plotting/block'+str(column_blocks)+'_'+str(row_blocks)+'gen'+str(generation)+'.txt',final_blocks,delimiter=',')




print("Final blocks: ")
print(final_blocks)
fitnessAndCityPlot(best_outputs,final_blocks, block_size, city_size, cmap)
if visualizations: grid_plot(block_size, city_size)