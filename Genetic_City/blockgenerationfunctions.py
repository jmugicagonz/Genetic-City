# -*- coding: utf-8 -*-

"""
 ██████╗ ███████╗███╗   ██╗███████╗████████╗██╗ ██████╗     ██████╗██╗████████╗██╗   ██╗
██╔════╝ ██╔════╝████╗  ██║██╔════╝╚══██╔══╝██║██╔════╝    ██╔════╝██║╚══██╔══╝╚██╗ ██╔╝
██║  ███╗█████╗  ██╔██╗ ██║█████╗     ██║   ██║██║         ██║     ██║   ██║    ╚████╔╝
██║   ██║██╔══╝  ██║╚██╗██║██╔══╝     ██║   ██║██║         ██║     ██║   ██║     ╚██╔╝
╚██████╔╝███████╗██║ ╚████║███████╗   ██║   ██║╚██████╗    ╚██████╗██║   ██║      ██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝     ╚═════╝╚═╝   ╚═╝      ╚═╝

Functions used for generation of new cities and populations for algorithm.

By: Juan Mugica - jmugicag@mit.edu
MIT Media Lab - City Science Group
                                                                                      """

import numpy as np
from progressbar import printProgressBar #Import progress bar function.
from random import *

#Function creates a random city design by assigning a specific number to each block.
#Number key is based on the block representation used on the Bento Scope.
#TODO: This function should be rethought as evey number between 0->1.49 will go to 1, being the result not an uniform distribution. -> CHANGE
def blockgen(desired_size, types):
    block = np.random.randint(1,types+1,(desired_size,desired_size))
    block = np.reshape(block, desired_size * desired_size) #Reshapes matrix into a single vector for better management.
    return (block)

#Function creates a matrix with a specific number of cities and size.
#Number of cities is the total population of cities for the algorithm.
def create_population(population_size, block_size, uses):
    printProgressBar(0, population_size, prefix = 'Population Generation Progress:', suffix = 'Complete', length = 50) #Progress bar for terminal interface.
    matrix = np.arange(block_size * block_size) #Creates empty vector to be used to create matrix.
    for indiv in range(0, population_size):
        newblock = blockgen(block_size, uses) #Calls new city generator.
        matrix = np.vstack((matrix, newblock)) #Adds new city to complete population matrix.
        printProgressBar(indiv + 1, population_size, prefix = 'Population Generation Progress:', suffix = 'Complete', length = 50) #Progress bar for terminal interface.
    matrix = np.delete(matrix, 0, 0) #Deletes fisrt row used as placeholder.
    return matrix #Returns matrix with each row representing a different city.
