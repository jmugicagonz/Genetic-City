from itertools import groupby, product
import numpy as np
import copy
from parameters import *
from initFunctions import *

"3"    
def test_green_space_balance_width(solution,distance_table):
    #First we find in the solution which indexes correspond to parks
    parks = np.where(solution == 1)[0]
    #We initialize the fitness function to 0
    fitness = 0
    if len(parks)>0:
        #From those indexes which are parks, which of them are adjacent?
        man_tups = [sorted(sub) for sub in product(parks, repeat = 2)
                                                if distance_table[sub[0],sub[1]] == 1]
        #We create a dictionary with those chains of adjacent points
        res_dict = {ele: {ele} for ele in parks}
        new_res_dict = copy.deepcopy(res_dict)
        new_man_tups = []
        for tup1, tup2 in man_tups:
            new_man_tups.append((tup1,tup2))
            new_man_tups.append((tup2,tup1))
        for tup1,tup2 in new_man_tups:
            new_res_dict[tup1] |= res_dict.get(tup2)
        #Now we will prize those nodes being connected to multiple other nodes
        fitness += sum(np.exp(len(cluster)-1) for cluster in new_res_dict.values() if len(cluster)>1)
    print("Fitness green space balance width: ", coef_green_space_balance_width*fitness)

"4"    
def test_diversity_of_housing(solution,distance_table):
    #First we find in the solution which indexes correspond to residences
    houses = np.where(solution == 3)[0]
    #We initialize the fitness function to 0
    fitness = 0
    if len(houses)>0:
        #From those indexes which are houses, which of them are adjacent?
        man_tups = [sorted(sub) for sub in product(houses, repeat = 2)
                                                if distance_table[sub[0],sub[1]] == 1]
        #We create a dictionary with those chains of adjacent points
        res_dict = {ele: {ele} for ele in houses}
        for tup1, tup2 in man_tups:
            res_dict[tup1] |= res_dict[tup2]
            res_dict[tup2] = res_dict[tup1]
        #Creation of arrays containing those adjacent chains. We take the unique values from the dictionary.
        res = [[*next(val)] for key, val in groupby(
                sorted(res_dict.values(), key = id), id)]
    counter_medium = 0.0
    counter_large = 0.0
    for residence_area in res:
        size = len(residence_area)
        if size>=3:
            counter_large += 1
        elif size>=2:
            counter_medium += 1
    percentage_large = counter_large/len(houses)
    percentage_medium = counter_medium/len(houses)
    percentage_small = 1 - (percentage_large+percentage_medium)
    print("Percentage large: {} with objective {}".format(percentage_large,percentage_large_housing))
    print("Percentage medium: {} with objective {}".format(percentage_medium,percentage_medium_housing))
    print("Percentage small: {} with objective {}".format(percentage_small,percentage_small_housing))
    fitness = nd_small_house.pdf(percentage_small)+nd_medium_house.pdf(percentage_medium)+nd_large_house.pdf(percentage_large)
    print("Fitness for diversity of housing: ", coef_diversity_of_housing*fitness)