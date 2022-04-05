from itertools import groupby, product
import numpy as np
import copy
from parameters import *
from connections import *
from parameters import *

"1"
"Refers to things that should be closer to the road. Office +2, Housing +1, Park + 0"
def acces(solution,unique,counts,lists_of_distances):
    fitness = 0
    #The followed strategy computs the minimum distance from each ammenity to any different ammenity, as roads are now separating amenities.
    min_distances_accesibility_home = np.minimum(lists_of_distances[0],lists_of_distances[1])
    min_distances_accesibility_office = np.minimum(lists_of_distances[2],lists_of_distances[3])
    mean_of_all_distances = (2*np.mean(min_distances_accesibility_office) + np.mean(min_distances_accesibility_home))/3
    fitness = 1/mean_of_all_distances
    return fitness*coef_accessibility
#The fitness function will return a greater value if number of parks increases. Should converge into more parks.

"2"
def green_amount(solution,unique,counts,lists_of_distances):
    green_sq_meters_people_living = len(np.where(solution==3))*residence_density*park_space_per_person
    sq_meters_of_parks = len(np.where(solution==3))*625
    if(sq_meters_of_parks>=green_sq_meters_people_living): return 100
    fitness = sq_meters_of_parks/green_sq_meters_people_living*100
    return fitness

"3"
def green_width(solution,unique,counts,lists_of_distances):
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
        #As tuples are automatically created with tuple1<tuple2, we now create a dictionary which tuples having tuple1<tuple2 and tuple1>tuple2, to find every cluster in the matrix.
        for tup1, tup2 in man_tups:
            new_man_tups.append((tup1,tup2))
            new_man_tups.append((tup2,tup1))
        for tup1,tup2 in new_man_tups:
            new_res_dict[tup1] |= res_dict.get(tup2)
        #Now we will prize those nodes being connected to multiple other nodes
        fitness += sum(pow(len(cluster),2) for cluster in new_res_dict.values() if len(cluster)>1) ####np.exp(len(cluster)-1)
    corners = 4*pow(3,2)
    ideal_park_size = int(np.sqrt(len(parks)))
    edge_rows_and_columns = 4*(ideal_park_size-2)*pow(5,2)
    inside = (ideal_park_size*ideal_park_size-4*ideal_park_size)*pow(8,2)
    max_green_space_balance_width = corners+edge_rows_and_columns+inside
    coef_green_space_balance_width = 2/max_green_space_balance_width*100
    fitness = coef_green_space_balance_width*fitness
    if (fitness>=100): return 100
    return fitness

"4"    
def div_h(solution,unique,counts,lists_of_distances):
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
        if size>=size_large_house:
            counter_large += 1
        elif size>=size_medium_house:
            counter_medium += 1
    percentage_large = counter_large/len(houses)
    percentage_medium = counter_medium/len(houses)
    percentage_small = 1 - (percentage_large+percentage_medium)
    fitness = nd_small_house.pdf(percentage_small)+nd_medium_house.pdf(percentage_medium)+nd_large_house.pdf(percentage_large)
    fitness *=1.5
    if(fitness>=100): return 100
    return coef_diversity_of_housing*fitness

"5"
def div_o(solution,unique,counts,lists_of_distances):
    #First we find in the solution which indexes correspond to residences
    offices = np.where(solution == 2)[0]
    #We initialize the fitness function to 0
    fitness = 0
    if len(offices)>0:
        #From those indexes which are offices, which of them are adjacent?
        man_tups = [sorted(sub) for sub in product(offices, repeat = 2)
                                                if distance_table[sub[0],sub[1]] == 1]
        #We create a dictionary with those chains of adjacent points
        res_dict = {ele: {ele} for ele in offices}
        for tup1, tup2 in man_tups:
            res_dict[tup1] |= res_dict[tup2]
            res_dict[tup2] = res_dict[tup1]
        #Creation of arrays containing those adjacent chains. We take the unique values from the dictionary.
        res = [[*next(val)] for key, val in groupby(
                sorted(res_dict.values(), key = id), id)]
    counter_medium = 0.0
    counter_large = 0.0
    for office_area in res:
        size = len(office_area)
        if size>=size_large_office:
            counter_large += 1
        elif size>=size_medium_office:
            counter_medium += 1
    percentage_large = counter_large/len(offices)
    percentage_medium = counter_medium/len(offices)
    percentage_small = 1 - (percentage_large+percentage_medium)
    fitness = nd_small_office.pdf(percentage_small)+nd_medium_office.pdf(percentage_medium)+nd_large_office.pdf(percentage_large)
    fitness *= 1.5
    if(fitness>=100): return 100
    return coef_diversity_of_housing*fitness

"6"
"Takes the closest office to each residence, without taking in account if people will fit in those offices (like a vertical no limit density)"
def h_o_walk(solution,unique,counts,lists_of_distances):
    fitness = 0
    fitness=1/(np.mean(lists_of_distances[0]))
    return coef_house_office_walkable*fitness

"7"
"Houses count double in this acces to parks"
def acc_p(solution,unique,counts,lists_of_distances):
    fitness = 0
    mean_of_all_distances = (2*np.mean(lists_of_distances[1]) + np.mean(lists_of_distances[3]))/3
    fitness = 1/mean_of_all_distances
    return fitness*coef_access_to_parks


"8"
"There will be more balance if the number of people living and working is compensated"
def h_o_balance(solution,unique,counts,lists_of_distances):
    nb_people_living = len(np.where(solution==3))*residence_density
    nb_people_working = len(np.where(solution==2))*office_density
    if (nb_people_living<=nb_people_working): fitness=nb_people_living/nb_people_working*100
    else: fitness=nb_people_working/nb_people_living*100
    return fitness

"9"
def peop_fit(solution, unique, counts,lists_of_distances):
    if (len(np.where(solution == 3)[0])<min_num_people_to_fit/residence_density): return 0 #This solution can't fit the number of people needed
    return 100

"10"
def dist_h_o_p(solution):
    parks = np.where(solution == 1)
    offices = np.where(solution == 2)
    homes = np.where(solution == 3)
    distances_homes_to_offices = np.zeros(int(homes[0].shape[0]))
    distances_homes_to_parks = np.zeros(int(homes[0].shape[0]))
    distances_offices_to_homes = np.zeros(int(offices[0].shape[0]))
    distances_offices_to_parks = np.zeros(int(offices[0].shape[0]))

    for home in range(int(homes[0].shape[0])):
        min_distance_to_office = max_distance
        min_distance_to_park = max_distance
        for office in range(offices[0].shape[0]):
            distance_to_office = distance_table[homes[0][home], offices[0][office]]
            if(distance_to_office<min_distance_to_office): min_distance_to_office=distance_to_office
            if min_distance_to_office==1: break
        distances_homes_to_offices[home]=min_distance_to_office
        for park in range(parks[0].shape[0]):
            distance_to_park = distance_table[homes[0][home], parks[0][park]]
            if(distance_to_park<min_distance_to_park): min_distance_to_park=distance_to_park
            if min_distance_to_park==1: break
        distances_homes_to_parks[home]=min_distance_to_park
        

    for office in range(int(offices[0].shape[0])):
        min_distance_to_home = max_distance
        min_distance_to_park = max_distance
        for home in range(homes[0].shape[0]):
            distance_to_home = distance_table[offices[0][office], homes[0][home]]
            if(distance_to_home<min_distance_to_home): min_distance_to_home=distance_to_home
            if min_distance_to_home==1: break
        distances_offices_to_homes[office]=min_distance_to_home
        for park in range(parks[0].shape[0]):
            distance_to_park = distance_table[offices[0][office], parks[0][park]]
            if(distance_to_park<min_distance_to_park): min_distance_to_park=distance_to_park
            if min_distance_to_park==1: break
        distances_offices_to_parks[office]=min_distance_to_park
    return distances_homes_to_offices, distances_homes_to_parks, distances_offices_to_homes, distances_offices_to_parks

#Creation of the set for rules.
def create_set_rules():
    set_rules = {acces,green_amount,green_width,div_h,div_o,h_o_walk,acc_p,h_o_balance,peop_fit}
    return set_rules