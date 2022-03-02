from numpy import block
from parameters import *
import scipy.stats


def function_save_parameters(path_results):
    parameters_file = open(path_to_code+"/parameters.py", 'r')
    lines = parameters_file.readlines()
    with open(path_results+'/parameters.txt', 'w') as f:
        f.write('\n'.join(lines))
    return

# Matrix with the block size and where each element is equal to the tuple that gives its position
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

#Create dictionary for images saving
dictionary_images = {i:chr(i+96) for i in range(1,27)}

#Normal distributions for housing
nd_small_house = scipy.stats.norm(percentage_small_housing, 0.2)
nd_medium_house = scipy.stats.norm(percentage_medium_housing, 0.2)
nd_large_house = scipy.stats.norm(percentage_large_housing, 0.2)

#Normal distributions for offices
nd_small_office = scipy.stats.norm(percentage_small_office, 0.2)
nd_medium_office = scipy.stats.norm(percentage_medium_office, 0.2)
nd_large_office = scipy.stats.norm(percentage_large_office, 0.2)

#Normal distribution for roads
nd_roads = scipy.stats.norm(1,1)

#Coeficients of regularization for fitness functions
#corners = 4*pow(3,2)
#edge_rows_and_columns = 4*(block_size*city_size-2)*pow(5,2)
#inside = (block_size*block_size*city_size*city_size-4*block_size*city_size)*pow(8,2)
#max_green_space_balance_width = corners+edge_rows_and_columns+inside
#coef_green_space_balance_width = 1/max_green_space_balance_width*100

max_diversity_of_housing = nd_small_house.pdf(percentage_small_housing)+nd_medium_house.pdf(percentage_medium_housing)+nd_large_house.pdf(percentage_large_housing)
coef_diversity_of_housing = 1/max_diversity_of_housing*100

coef_adjacent_roads = 1/(nd_roads.pdf(1))*100

coef_accessibility = 100

max_distance = np.max(distance_table)
coef_house_office_walkable = 100
coef_access_to_parks = 100




