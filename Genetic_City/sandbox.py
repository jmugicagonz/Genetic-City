import numpy as np
import copy
from itertools import groupby, product
from initFunctions import *
from parameters import *

solution = np.asarray([1,1,1,1,1,1,2,2,3,3,2,2,3,1,3,3])
#First we find in the solution which indexes correspond to parks
parks = np.where(solution==1)[0]
print("Parks are: {}".format(parks))
#We initialize the fitness function to 0
fitness = 0
if len(parks)>0:
    #From those indexes which are parks, which of them are adjacent?
    man_tups = [sorted(sub) for sub in product(parks, repeat = 2)
                                            if distance_table[sub[0],sub[1]] == 1]
    print("Man tups are: {}".format(man_tups))
    #We create a dictionary with those chains of adjacent points
    res_dict = {ele: {ele} for ele in parks}
    print("Res dict is: {}".format(res_dict))
    new_res_dict = copy.deepcopy(res_dict)
    new_man_tups = []
    #As tuples are automatically created with tuple1<tuple2, we now create a dictionary which tuples having tuple1<tuple2 and tuple1>tuple2, to find every cluster in the matrix.
    for tup1, tup2 in man_tups:
        new_man_tups.append((tup1,tup2))
        new_man_tups.append((tup2,tup1))
    for tup1,tup2 in new_man_tups:
        new_res_dict[tup1] |= res_dict.get(tup2)
    print("New man tups are: {}".format(new_man_tups))
    print("New res dict are: {}".format(new_res_dict))
    #Now we will prize those nodes being connected to multiple other nodes
    fitness += sum(pow(len(cluster),2) for cluster in new_res_dict.values() if len(cluster)>1) ####np.exp(len(cluster)-1)
    print("Fitness is: {}".format(fitness))
corners = 4*pow(3,2)
ideal_park_size = int(np.sqrt(len(parks)))
edge_rows_and_columns = 4*(ideal_park_size-2)*pow(5,2)
inside = (ideal_park_size*ideal_park_size-4*ideal_park_size)*pow(8,2)
max_green_space_balance_width = corners+edge_rows_and_columns+inside
coef_green_space_balance_width = 2/max_green_space_balance_width*100
fitness = coef_green_space_balance_width*fitness