import numpy as np
from blockgenerationfunctions import *                                          #Functions for creating new city arrays.
from fitnessFunctions import *                                                  #Functions for evaluation fitness of cities.
from crossfunctions import *                                                    #Functions for crossing individuals.
from mutation_functions import *                                                #Functions for mutating individuals.
from selectionFunctions import *                                                #Functions for best individual selection.
from parameters import *
from brix import Handler                                                        #Module to communicate with the CityIO


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


    def compute_generation(self):
        fitness_vector, list_of_dictionaries_rules = evaluate_blocks(self.population_matrix, dictionary_rules)
        best_match_idx = np.where(fitness_vector == np.max(fitness_vector))
        best_value = np.max(fitness_vector)
        self.best_outputs.append(best_value)

        # Selecting the best parents in the population for mating.
        parents = select_mating_pool(fitness_vector, self.population_matrix, num_parents_mating)

        #Cross
        offspring_crossover = crossover(parents,offspring_size=(population_size-parents.shape[0], block_size*block_size),crossover_value=crossover_value)

        # Adding some variations to the offspring using mutation.
        offspring_mutation = mutation(offspring_crossover, prob_mutation, block_size, building_types)

        # Creating the new population based on the parents and offspring.
        self.population_matrix[0:parents.shape[0], :] = parents
        self.population_matrix[parents.shape[0]:, :] = offspring_mutation