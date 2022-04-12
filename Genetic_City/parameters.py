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
block_size = 7 # Size of the area to optimise (square dimension)
building_types = 3 # [1 = Campus, 2 = Industry, 3 = Residence]
cmap = ListedColormap(["forestgreen","lightcoral","lightgray","dimgray"])

"Values to define land uses and initialise the connection to the table"
dict_landUses = {1: 'Campus', 2: 'Industrial', 3: 'Residential'}

""
visualizations = True # True: Images should be saved. False otherwise
path_to_code = "C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City"

'''PARAMETERS FOR RULES'''

"Weights for rules: "
'''weights = np.array( #Weights used by function to evaluate. Places more interest in high numbers.
    [1, #1: accesibility
    1, #2: green_space_balance_amount 
    60, #3: green_space_balance_width
    30, #4: diversity_of_housing
    30, #5: diversity_of_office
    1, #6: house_office_walkable
    1, #7: access_to_parks
    1, #8: house_office_balance
    1, #9: people_fitting
    1, ]) #10: distances_homes_offices_parks'''

"Population/Area parameters for rules"
min_num_people_to_fit = 3000 #Minimum number of people to fit in the space
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
target_dict_housing = [percentage_small_housing, percentage_medium_housing, percentage_large_housing]

"Rule 5: Diversity of office"
#Size of office >= (e.g: size_large_office = 3 means that every office composed by 3 or more nodes will be considered large)
size_large_office = 3
size_medium_office = 2
#All the rest will be considered small offices

#The next three percentages should sum 1
percentage_small_office = 0.2
percentage_medium_office = 0
percentage_large_office = 0.8
target_dict_office = [percentage_small_office, percentage_medium_office, percentage_large_office]

'''PARAMETERS FOR PLOTS'''
num_generations_saved = 20 # >=1
time_per_image = 500 #Time in ms for each image in the GIF
save_data = False


'''PARAMETERS ARUCO TAGS'''
id_play = 227 # Id of the Aruco tag representing the play buttong
id_pause = 128 # Id of the Aruco tag representing the pause button
<<<<<<< HEAD
id_block = 12 # Id of the Aruco tag representing the block cell
pos_play_pause = 49 # Position of the Aruco tag for the play/pause button

=======
id_block = 12 # Id of the Aruco tag representing the block button
id_campus = 3 # Id of the Aruco tag representing the campus button
id_industry = 8 # Id of the Aruco tag representing the industry button
id_residence = 19 # Id of the Aruco tag representing the residence button
pos_play_pause = 49 # Position of the Aruco tag for the play/pause button
>>>>>>> c7dbb504687dc3862f32bee15490f75b0626535b
