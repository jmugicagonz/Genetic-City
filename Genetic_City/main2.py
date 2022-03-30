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
import keyboard                                                                 #Library for stopping the code when pressing a letter
from brix import Handler                                                        #Module to communicate with the CityIO
import random                                                                   #Used to send random heights of buildings
from statemachine import State, StateMachine                                    #We import the state machine library to govern the whole program
import socket                                                                   #Library to read from server
import sys                                                                      #Library to read from server


'''FUNCTION TO UPDATE THE ONLINE GRID'''
def update_land_uses(geogrid_data, grid_list=[0], dict_landUses={0: '0'}, height=1):
    for cell in geogrid_data:
        #cell['name'] = dict_landUses[grid_list[cell['id']]]
        randomTall = random.uniform(0,1)
        randomH = random.randint(0,height)
        cell['name'] = dict_landUses[grid_list[cell['id']]]
        if cell['name'] == 'Industrial': 
            if randomTall >= 0.8: cell['height'] = 4*randomH
            else: cell['height'] = 2*randomH
        elif cell['name'] == 'Residential': 
            if randomTall >= 0.8: cell['height'] = randomH
            else: cell['height'] = 2*randomH
        elif cell['name'] == 'Campus': cell['height'] = 0
    return geogrid_data


#Placeholder variables
population_matrix = np.arange(block_size * block_size) # Matrix for storing populations within process.
selected_matrix = np.zeros((population_size, block_size*block_size)) # Matrix for selected populations within process.
final_blocks = np.zeros((block_size,block_size)) # Matrix for storing the best blocks coming from the last iteration
so_far_blocks = np.zeros((block_size,block_size)) # Matrix for storing the best blocks coming from some iterations and see the progress

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

#Values to define land uses and initialise the connection to the table
dict_landUses = {1: 'Campus', 2: 'Industrial', 3: 'Residential'}
table_name = 'geneticcity'
H = Handler(table_name)

#Initialise generations
generation = 0
#START OF GENERATON LOOP ################################################################################################################
try:
    while True:
        if generation%5==0:
            print("Press 'c' to continue")
            print("Press 'e' to calibrate the table")
            ch = input("['c','e']>>>")
        
            if ch == "e":
                break   

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

        if generation%5 == 0: #Send values each three generations
            max_height = 500
            H.update_geogrid_data(update_land_uses, grid_list=parents[0, :], dict_landUses=dict_landUses, height=max_height)

        generation +=1
        if keyboard.is_pressed("c"):
            break 
except KeyboardInterrupt:
    print("Stopped with ctrl+c at iteration {}".format(generation))

print("Stopped with c at iteration {}".format(generation))
print("Please calibrate the table")


ip = '127.0.0.1'
port = 15800
# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (ip, port)
s.bind(server_address)

while True:
    print("Press 'c' to continue")
    print("Press 'e' to exit")

    ch = input("['c','e']>>>")

    if ch == "c":
        data1, address = s.recvfrom(4096)
        print("Data1 now is: {}".format(data1))
    elif ch == "e":
        break

print("Data selected is: {}".format(data1))






'''# Getting the best solution after iterating finishing all generations.
#At first, the fitness is calculated for each solution in the final generation.
fitness_vector, list_of_dictionaries_rules = evaluate_blocks(population_matrix, dictionary_rules) # Then return the index of that solution corresponding to the best fitness.
best_match_idx = np.where(fitness_vector == np.max(fitness_vector))'''