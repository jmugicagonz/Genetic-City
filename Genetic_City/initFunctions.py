import scipy.stats
from scipy.spatial.distance import cityblock

from parameters import *

# Matrix with the block size and where each element is equal to the tuple that gives its position. Used for Manhattan lookUp matrix
def block_matrix(grid_size):
    reshaped = np.reshape([[i,j] for i in range(grid_size) for j in range(grid_size)],(grid_size,grid_size,1,2))
    return [[i,j] for i in range(grid_size) for j in range(grid_size)]

# Matrix containing the manhattan distance between two indexes
def manhattan_table(block_matrix):
    return scipy.spatial.distance_matrix(block_matrix,block_matrix,p=1)

#Calculation of look_up distance table
distance_table  = manhattan_table(block_matrix(block_size))

#Calculation of look_up distance table matrix with roads
distance_table_roads  = manhattan_table(block_matrix((block_size)*2-1))

#Normal distributions for housing
nd_small_house = scipy.stats.norm(percentage_small_housing, 0.2)
nd_medium_house = scipy.stats.norm(percentage_medium_housing, 0.2)
nd_large_house = scipy.stats.norm(percentage_large_housing, 0.2)

#Normal distributions for offices
nd_small_office = scipy.stats.norm(percentage_small_office, 0.2)
nd_medium_office = scipy.stats.norm(percentage_medium_office, 0.2)
nd_large_office = scipy.stats.norm(percentage_large_office, 0.2)

#Calculation of rules coefficients
max_diversity_of_housing = nd_small_house.pdf(percentage_small_housing)+nd_medium_house.pdf(percentage_medium_housing)+nd_large_house.pdf(percentage_large_housing)
coef_diversity_of_housing = 1/max_diversity_of_housing*100
coef_accessibility = 100
max_distance = np.max(distance_table)
coef_house_office_walkable = 100
coef_access_to_parks = 100

#Function to calculate the diversity

def manhattan_dist_diversity(case_dict, target_dict):
    if len(case_dict)==0:
        return None
    case_counts=[case_dict[s] if s in case_dict else 0 for s in target_dict]
    target_counts=[target_dict[s] for s in target_dict]
    max_deviation=sum([max(c, 1-c) for c in target_counts])
    return 1-cityblock(case_counts, target_counts)/max_deviation





