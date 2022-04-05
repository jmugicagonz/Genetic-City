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

import keyboard  # Library for stopping the code when pressing a letter
import matplotlib.pyplot as plt  # Plotting
import numpy as np  # Matrix and array handling.
import ray

from connections import *  # Import functions for including roads
from initFunctions import *  # Import initial calculations
from mainMachine import MainMachine
from plotting import *  # Functions for plotting

#Initialise the Main Machine
mainMachine = MainMachine()

#Create list to store fitness for different rules
fitness_rules_solutions = []

# Starting Ray for parallelization
ray.init()

#START OF GENERATON LOOP
mainMachine.start()

#START THE CALIBRATION OF THE TABLE
mainMachine.calibrate()

#BEGIN INTERACTION WITH PIECES
mainMachine.interact()

'''# Getting the best solution after iterating finishing all generations.
#At first, the fitness is calculated for each solution in the final generation.
fitness_vector, list_of_dictionaries_rules = evaluate_blocks(population_matrix, dictionary_rules) # Then return the index of that solution corresponding to the best fitness.
best_match_idx = np.where(fitness_vector == np.max(fitness_vector))'''
