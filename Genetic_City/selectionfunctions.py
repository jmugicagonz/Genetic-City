# -*- coding: utf-8 -*-

"""
 ██████╗ ███████╗███╗   ██╗███████╗████████╗██╗ ██████╗     ██████╗██╗████████╗██╗   ██╗
██╔════╝ ██╔════╝████╗  ██║██╔════╝╚══██╔══╝██║██╔════╝    ██╔════╝██║╚══██╔══╝╚██╗ ██╔╝
██║  ███╗█████╗  ██╔██╗ ██║█████╗     ██║   ██║██║         ██║     ██║   ██║    ╚████╔╝
██║   ██║██╔══╝  ██║╚██╗██║██╔══╝     ██║   ██║██║         ██║     ██║   ██║     ╚██╔╝
╚██████╔╝███████╗██║ ╚████║███████╗   ██║   ██║╚██████╗    ╚██████╗██║   ██║      ██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝     ╚═════╝╚═╝   ╚═╝      ╚═╝

Functions used for selection of best individuals in algorithnm.

By: Juan Mugica - jmugicag@mit.edu
MIT Media Lab - City Science Group
                                                                                      """

import numpy as np
from progressbar import printProgressBar #Import progress bar function.



def select_mating_pool(fitness_vector,population, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = np.empty((num_parents, population.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = np.where(fitness_vector == np.max(fitness_vector))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = population[max_fitness_idx, :]
        fitness_vector[max_fitness_idx] = -99999
    return parents



'''


def select_cities_rough(city_to_ev, input_city_pop, population, citysize, best_ind, best_ev):

    selected_population_matrix = np.zeros((population, citysize*citysize))
    print('This is the best ev: ', city_to_ev[np.argmax(city_to_ev)])

    if city_to_ev[np.argmax(city_to_ev)] > best_ev:
        best = np.argmax(city_to_ev)
        selected_population_matrix[0:int(population*.5)] = input_city_pop[best]
        city_to_ev[best] = 0

        best = np.argmax(city_to_ev)
        selected_population_matrix[int(population*.5):int(population*.8)] = input_city_pop[best]
        city_to_ev[best] = 0

        #TODO: review if put random part here -> can play with this
        best = np.argmax(city_to_ev)
        selected_population_matrix[int(population*.8):int(population)] = input_city_pop[best]
    else:
        selected_population_matrix[0:int(population*.5)] = best_ind

        #TODO: review if we keep the best found individual as the reference and what do we do with the rest
        best = np.argmax(city_to_ev)
        selected_population_matrix[int(population*.5):int(population*.8)] = input_city_pop[best]
        city_to_ev[best] = 0

        best = np.argmax(city_to_ev)
        selected_population_matrix[int(population*.8):int(population)] = input_city_pop[best]

    return selected_population_matrix
'''