import numpy as np
from random import *
from progressbar import printProgressBar #Import progress bar function.



def mutate_individual(input_city, mut_prob, types): #Mutates chromosomically each individual depending on a given probability.
    for genes in range(0, input_city.shape[0]):
        #TODO: is this != 0 necessary? -> can be removed
        if random() < mut_prob:
            #place_variable = randint(1,9)
            input_city[genes] = randint(1,types)
    return input_city

def mutation(offspring_crossover, prob_mutation, block_size,building_types): #Complete function for looping through every individual's mutations in an entire population.
    offspring_size = offspring_crossover.shape[0]
    mutated_population = np.zeros((offspring_size, block_size*block_size))
    printProgressBar(0, offspring_size, prefix = 'Population Mutation Progress:', suffix = 'Complete', length = 50)
    for indiv in range (0, offspring_size):
        mutated_individual = mutate_individual(offspring_crossover[indiv, :], prob_mutation, building_types)
        mutated_population[indiv, :] = mutated_individual
        printProgressBar(indiv + 1, offspring_size, prefix = 'Population Mutation Progress:', suffix = 'Complete', length = 50)
    return mutated_population
