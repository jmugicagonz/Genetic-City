from itertools import groupby, product
import numpy as np

def accesibility():
    return
def green_space_balance_amount(no_parks,no_blocks,percentage_obj):
    '''percentage = no_parks/no_blocks
    if percentage < percentage_obj:
        fitness = percentage-percentage_obj
    if percentage > percentage_obj:
        fitness = percentage_obj-percentage'''
    fitness = no_parks/no_blocks
    return fitness
def green_space_balance_width(solution,distance_table):
    parks = np.where(solution == 3)[0]
    if len(parks)>0:
        man_tups = [sorted(sub) for sub in product(parks, repeat = 2)
                                                if distance_table[sub[0],sub[1]] == 1]
        res_dict = {ele: {ele} for ele in parks}
        for tup1, tup2 in man_tups:
            res_dict[tup1] |= res_dict[tup2]
            res_dict[tup2] = res_dict[tup1]
        
        res = [[*next(val)] for key, val in groupby(
                sorted(res_dict.values(), key = id), id)]

        distances = 0
        total=0
        for i in range(int(len(res))):
            man_tups = [sorted(sub) for sub in product(res[i], repeat = 2) if distance_table[sub[0],sub[1]] >= 1]
            for j in man_tups:
                if len(j)>1:
                    distances+=distance_table[j[0],j[1]]
                    total+=1
        fitness = 1/(res.__len__())
        if total>0 : 
            distances/=total
            fitness += 1/distances
    else: fitness = 0
    return fitness
def diversity_of_housing():
    return
def diversity_of_office():
    return
def house_office_walkable():
    return
def access_to_parks():
    return
def house_office_balance():
    return
def green_space():
    return