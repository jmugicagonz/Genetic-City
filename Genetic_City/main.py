
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
from connections import *                                                       #Import functions for including roads
from testRules import *                                                         #Import functions for testing rules
from initFunctions import *                                                     #Import initial calculations


#Placeholder variables
population_matrix = np.arange(block_size * block_size) # Matrix for storing populations within process.
selected_matrix = np.zeros((population_size, block_size*block_size)) # Matrix for selectec populations within process.
gen = np.arange(num_generations) + 1
final_blocks = np.zeros((block_size*city_size,block_size*city_size )) # Matrix for storing the best blocks coming from the last iteration
so_far_blocks = np.zeros((block_size*city_size,block_size*city_size )) # Matrix for storing the best blocks coming from some iterations and see the progress

#Creation of dictionary for rules
dictionary_rules = create_dictionary_rules()

#TODO: make it support multiple columns
best_outputs = []

#Variable for when to save images and plots
generation_to_save = int(num_generations / num_generations_saved)

#Creation of directories to save images and plots
path_results, path_images_solution, path_images_fitness, path_images_radar, path_images_gif, path_plotting = create_directory_images()

#Save parameters in parameters.txt
function_save_parameters(path_results)

#Define counter for plotting, fitness and radar
counter1 = 1
counter2 = 1
counter3 = 1

#Create list to store fitness for different rules
fitness_rules_solutions = []

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

            fitness_vector, list_of_dictionaries_rules = evaluate_blocks(population_matrix, dictionary_rules)
            best_match_idx = np.where(fitness_vector == np.max(fitness_vector))
            best_value = np.max(fitness_vector)
            best_outputs.append(best_value)

            if((generation % generation_to_save)==0):
                so_far_blocks[row_blocks*block_size:(row_blocks*block_size)+block_size, column_blocks*block_size:(column_blocks*block_size)+block_size] = np.reshape(population_matrix[best_match_idx[0].shape[0], :], (block_size, block_size))
                matrix_with_roads = include_roads(so_far_blocks)
                matrix_with_roads_amplified = matrix_for_visualization(matrix_with_roads)
                saveImages(matrix_with_roads_amplified, best_outputs, cmap, generation,path_images_solution, path_images_fitness, path_plotting, num_generations, counter1, counter2,counter3, path_images_radar,list_of_dictionaries_rules[best_match_idx[0].shape[0]])
                counter1+=1
                counter2+=1
                counter3+=1

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

        print("Best solution : ", population_matrix[best_match_idx[0][0], :])
        print("Best solution fitness : ", fitness_vector[best_match_idx[0][0]])
        print("Fitness vector: ",fitness_vector)
        final_blocks[row_blocks*block_size:(row_blocks*block_size)+block_size, column_blocks*block_size:(column_blocks*block_size)+block_size] = np.reshape(population_matrix[best_match_idx[0][0], :], (block_size, block_size))
        #if visualizations: np.savetxt('C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City/plotting/block'+str(column_blocks)+'_'+str(row_blocks)+'gen'+str(generation)+'.txt',final_blocks,delimiter=',')




'''unique, counts = np.unique(final_blocks,return_index=False, return_inverse=False, return_counts=True, axis=None)
print("Number of parks: ")
print(counts[0])
print("Number of elements: ")
print(np.size(final_blocks))
print("Final proportion: ")
print(counts[0]/np.size(final_blocks))'''
matrix_with_roads = include_roads(final_blocks)
matrix_with_roads_amplified = matrix_for_visualization(matrix_with_roads)
#if visualizations: np.savetxt('C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City/plotting/block'+'solution_amplified'+'.txt',matrix_with_roads_amplified,delimiter=',')
#grid_plot(np.shape(matrix_with_roads_amplified)[0], cmap)
#fitness_plot(best_outputs)
#saveImages(matrix_with_roads_amplified, best_outputs, cmap)

#Create GIF for solution and fitness
#create_gifs(path_images_solution)
#create_gifs(path_images_fitness)

#Concatenate images and place them in the gif folfer
get_concat_h(path_images_solution, path_images_fitness, path_images_radar, path_images_gif)

#Create GIF for concatenated images
create_gifs(path_images_gif)

'''TEST RULES'''
print("Final blocks are: ")
print(final_blocks)
print("Best match index: ",best_match_idx[0][0])
test_diversity_of_housing(final_blocks.reshape(block_size*block_size),distance_table)
test_green_space_balance_width(final_blocks.reshape(block_size*block_size),distance_table)

