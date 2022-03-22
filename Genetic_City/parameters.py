# -*- coding: utf-8 -*-

"""
GENETIC CITY

Parameters and some functions to compute new parameters.

By: Juan Mugica - jmugicag@mit.edu
MIT Media Lab - City Science Group
                                                                                      """

from matplotlib.colors import ListedColormap
import numpy as np

'''GENERAL PARAMETERS'''

"Genetic Algorithm Parameters:"
population_size = 200 # Number of solutions in the population.
num_parents_mating = 10 # Number of solutions to be selected as parents in the mating pool. Must be < population_size
num_generations = 400 # Number of generations.
prob_mutation = .1 # Must be between 0 and 1
crossover_value = .9 # The point at which crossover takes place between two parents. Usually, it is at the center.

"City Parameters"
block_size = 15 # Size of the area to optimise (square dimension)
building_types = 3 # [1 = Park, 2 = Office, 3 = Residential]
cmap = ListedColormap(["forestgreen","lightcoral","lightgray","dimgray"])

""
visualizations = True # True: Images should be saved. False otherwise
path_to_code = "C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City"

'''PARAMETERS FOR RULES'''

"Weights for rules: "
weights = np.array( #Weights used by function to evaluate. Places more interest in high numbers.
    [1, #1: accesibility
    1, #2: green_space_balance_amount 
    60, #3: green_space_balance_width
    30, #4: diversity_of_housing
    30, #5: diversity_of_office
    1, #6: house_office_walkable
    1, #7: access_to_parks
    1, #8: house_office_balance
    1, #9: people_fitting
    1, ]) #10: distances_homes_offices_parks

"Population/Area parameters for rules"
min_num_people_to_fit = 5700 #Minimum number of people to fit in the space
residence_density = 100 #people/house_node
office_density = 150 #people/office_node
park_space_per_person = 4 #gren space ideally needed per person, in m2, with each node being 625m2
area_node = 625

"RULE1: green_space_balance_amount"
percentage_parks = 0.9

"Rule 4: Diversity of housing"
#Size of housing >= (e.g: size_large_house = 3 means that every house composed by 3 or more nodes will be considered large)
size_large_house = 3
size_medium_house = 2
#All the rest will be considered small houses

#The next three percentages should sum 1
percentage_small_housing = 0.2
percentage_medium_housing = 0
percentage_large_housing = 0.8

"Rule 5: Diversity of office"
#Size of office >= (e.g: size_large_office = 3 means that every office composed by 3 or more nodes will be considered large)
size_large_office = 3
size_medium_office = 2
#All the rest will be considered small offices

#The next three percentages should sum 1
percentage_small_office = 0.2
percentage_medium_office = 0
percentage_large_office = 0.8

'''PARAMETERS FOR PLOTS'''
num_generations_saved = 20 # >=1
time_per_image = 500 #Time in ms for each image in the GIF
save_data = False