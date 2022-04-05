from fitnessFunctions import *
from rules import *
import numpy as np

solution = np.array([3,1,1,2,3,1,2,1,2,1])
set_rules = create_set_rules()

fitness, dictionary_rules_fitness = fitness_func(solution, set_rules)
print("Fitness is: {}".format(fitness))
print("Dictionary of rules are: {}".format(dictionary_rules_fitness))