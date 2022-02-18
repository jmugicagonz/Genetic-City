from itertools import groupby, product
import numpy as np
import copy

def accesibility(solution,distance_table):
    fitness=0
    return fitness
#The fitness function will return a greater value if number of parks increases. Should converge into more parks.
def green_space_balance_amount(solution,distance_table):
    unique, counts = np.unique(solution,return_index=False, return_inverse=False, return_counts=True, axis=None)
    no_parks=counts[0]
    no_blocks=np.shape(solution)[0]
    fitness = no_parks/no_blocks*100
    return fitness

def green_space_balance_width(solution,distance_table):
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
    return fitness
    
def diversity_of_housing(solution,distance_table):
    fitness = 0
    return fitness
def diversity_of_office(solution,distance_table):
    fitness = 0
    return fitness
def house_office_walkable(solution,distance_table):
    fitness = 0
    return fitness
def access_to_parks(solution,distance_table):
    fitness = 0
    return fitness
def house_office_balance(solution,distance_table):
    fitness = 0
    return fitness
def green_space(solution,distance_table):
    fitness = 0
    return fitness

def create_dictionary_rules():
    dictionary_rules = {0:accesibility,1:green_space_balance_amount,2:green_space_balance_width,3:diversity_of_housing,4:diversity_of_office,5:house_office_walkable,6:access_to_parks,7:house_office_balance,8:green_space}
    return dictionary_rules

'''OLD TOP-DOWN SOLUTION. IT TAKES TOO MUCH TIME TO COMPUTE'''
'''def green_space_balance_width(solution,distance_table):
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
        for tup1, tup2 in man_tups:
            res_dict[tup1] |= res_dict[tup2]
            res_dict[tup2] = res_dict[tup1]
        #Creation of arrays containing those adjacent chains. We take the unique values from the dictionary.
        res = [[*next(val)] for key, val in groupby(
                sorted(res_dict.values(), key = id), id)]
        distances = 0
        total=0
        for i in range(int(len(res))):
            #To increase the size of parks, we will give more fitness to those parks which are areas instead of lines. For that, we compute distances between those nodes making part of the park.
            fitness += np.sum(10*len(res[i]))
            #man_tups now will be tuples of nodes from the same park
            man_tups = [sorted(sub) for sub in product(res[i], repeat = 2) if distance_table[sub[0],sub[1]] >= 1]
            for j in man_tups:
                if len(j)>1:
                    distances+=distance_table[j[0],j[1]]
                    total+=1
        if total>0 : 
            distances/=total
            fitness += 100/distances
    return fitness'''