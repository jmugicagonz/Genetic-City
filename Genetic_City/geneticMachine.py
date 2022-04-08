import numpy as np
from brix import Handler  # Module to communicate with the CityIO
import os

from parameters import *
# Functions for the Genetic Algorithm
from blockgenerationfunctions import *  # Functions for creating new city arrays.
from selectionfunctions import *  # Functions for best individual selection.
from crossfunctions import *  # Functions for crossing individuals.
from fitnessFunctions import *  # Functions for evaluation fitness of cities.
from mutation_functions import *  # Functions for mutating individuals.

class GeneticMachine():
    def __init__(self):
        #Placeholder variables
        self.population_matrix = np.arange(block_size * block_size) # Matrix for storing populations within process.
        self.selected_matrix = np.zeros((population_size, block_size*block_size)) # Matrix for selected populations within process.
        self.final_blocks = np.zeros((block_size,block_size)) # Matrix for storing the best blocks coming from the last iteration
        self.so_far_blocks = np.zeros((block_size,block_size)) # Matrix for storing the best blocks coming from some iterations and see the progress

        # Create Initial Population #################################
        self.population_matrix = create_population(population_size, block_size, building_types) #Creates new block.
        self.best_outputs = []
        self.list_of_dictionaries_rules = []

        #Creation of set for rules
        self.set_rules = create_set_rules()

        #Load weights for the genetic algorithm
        self.weights = [] # Placeholder for weights before loading them in the next line
        self.load_weights() # We load the weights for the first time
        self.bool_weights = False #Bool to manage when to load weights

    def compute_generation(self):
        if self.bool_weights:
            self.load_weights()
        fitness_vector, self.list_of_dictionaries_rules = evaluate_blocks(self.population_matrix, self.set_rules, self.weights)
        #If we want to plot the best value
        '''best_match_idx = np.where(fitness_vector == np.max(fitness_vector))
        best_value = np.max(fitness_vector)
        self.best_outputs.append(best_value)'''

        # Selecting the best parents in the population for mating.
        parents = select_mating_pool(fitness_vector, self.population_matrix, num_parents_mating)

        #Cross
        offspring_crossover = crossover(parents,offspring_size=(population_size-parents.shape[0], block_size*block_size),crossover_value=crossover_value)

        # Adding some variations to the offspring using mutation.
        offspring_mutation = mutation(offspring_crossover, prob_mutation, block_size, building_types)

        # Creating the new population based on the parents and offspring.
        self.population_matrix[0:parents.shape[0], :] = parents
        self.population_matrix[parents.shape[0]:, :] = offspring_mutation

    def continue_generation(self, given_proposal):
        new_random_population = create_population(num_parents_mating-1, block_size, building_types) #Creates new block.
        parents = np.arange(block_size * block_size) #Creates empty vector to be used to create matrix.
        parents = np.vstack((parents, given_proposal)) #Adds interacted city.
        parents = np.vstack((parents, new_random_population)) #Adds new random cities to complete the parents population
        parents = np.delete(parents, 0, 0) #Deletes fisrt row used as placeholder.

        #Cross
        offspring_crossover = crossover(parents,offspring_size=(population_size-parents.shape[0], block_size*block_size),crossover_value=crossover_value)
         
        #Adding some variations to the offspring using mutation.
        offspring_mutation = mutation(offspring_crossover, prob_mutation, block_size, building_types)
    
        # Creating the new population based on the parents and offspring.
        self.population_matrix[0:parents.shape[0], :] = parents
        self.population_matrix[parents.shape[0]:, :] = offspring_mutation

    def load_weights(self, file_loc=str(os.getcwd())+'\weights.txt'):
        with open(file_loc) as f:
            lines = f.readlines()
            weights = dict()
        for line in lines:
            no_newline = line.replace("\n","")
            splitted_line = no_newline.split(': ')
            weights[splitted_line[0]] = int(splitted_line[1])
        self.weights = weights
        self.bool_weights = False
        print("New weights are:  {}".format(self.weights))

    def set_bool_weights(self):
        self.bool_weights = True
        print("Self bool_weights set to: {}".format(self.bool_weights))
