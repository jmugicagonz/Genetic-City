# Python3 code to demonstrate working of
# Group Adjacent Coordinates
from itertools import groupby, product
import numpy as np
import scipy.spatial
import copy

# Matrix with the block size and where each element is equal to the tuple that gives its position
def block_matrix(grid_size):
    reshaped = np.reshape([[i,j] for i in range(grid_size) for j in range(grid_size)],(grid_size,grid_size,1,2))
    return [[i,j] for i in range(grid_size) for j in range(grid_size)]

# Matrix containing the manhattan distance between two indexes
def manhattan_table(block_matrix):
    return scipy.spatial.distance_matrix(block_matrix,block_matrix,p=1)

def green_space_balance_width(solution,distance_table):
    #First we find in the solution which indexes correspond to parks
    parks = np.where(solution == 1)[0]
    #We initialize the fitness function to 0
    fitness = 0
    if len(parks)>0:
        #From those indexes which are parks, which of them are adjacent?
        man_tups = [sorted(sub) for sub in product(parks, repeat = 2)
                                                if distance_table[sub[0],sub[1]] == 1]
        print("Man tups are: ")
        print(man_tups)
        #We create a dictionary with those chains of adjacent points
        res_dict = {ele: {ele} for ele in parks}
        new_res_dict = copy.deepcopy(res_dict)
        new_man_tups = []
        for tup1, tup2 in man_tups:
            new_man_tups.append((tup1,tup2))
            new_man_tups.append((tup2,tup1))
        for tup1,tup2 in new_man_tups:
            new_res_dict[tup1] |= res_dict.get(tup2)
        print(new_res_dict)
        #Now we will prize those nodes being connected to multiple other nodes
        fitness += sum(np.exp(len(cluster)-1) for cluster in new_res_dict.values() if len(cluster)>1)
        #Creation of arrays containing those adjacent chains. We take the unique values from the dictionary.
        '''res = [[*next(val)] for key, val in groupby(
                sorted(res_dict.values(), key = id), id)]
        print("Res is: ")
        print(res)
        distances = 0
        total=0'''
        '''for i in range(int(len(res))):
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
            fitness += 100/distances'''
    return fitness

test_matrix = np.asarray([3,3,1,2,3,1,1,3,3,1,1,3,3,3,3,3])
print("Test matrix is: ")
print(test_matrix)
distance_table  = manhattan_table(block_matrix(4))
print(green_space_balance_width(test_matrix,distance_table))