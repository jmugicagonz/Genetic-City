from statemachine import StateMachine, State
import keyboard                                                                 #Library for stopping the code when pressing a letter
from onlineGrid import *                                                        #Import functions to support online grid
from parameters import *



import numpy as np                                                              #Matrix and array handling.
import matplotlib.pyplot as plt                                                 #Plotting

from plotting import *                                                          #Functions for plotting
from connections import *                                                       #Import functions for including roads
from initFunctions import *                                                     #Import initial calculations
import keyboard                                                                 #Library for stopping the code when pressing a letter
import ray

class MainMachine(StateMachine):
    initialized = State('Initialized', initial=True)
    computing_generations = State('Computing')
    user_interacting = State('Interacting')

    start = initialized.to(computing_generations)
    stop = computing_generations.to(user_interacting)
    resume = user_interacting.to(computing_generations)

    #Initialise the Genetic Machine
    genMachine = GeneticMachine()

    table_name = 'geneticcity'
    H = Handler(table_name)
    generation = 0

    def on_start(self):
        while True:
            if self.generation%5==0:
                print("Press 'c' to continue")
                print("Press 'e' to go and calibrate the table")
                ch = input("['c','e']>>>")
            
                if ch == "e":
                    break   

            print("Generation : ", self.generation)

            self.genMachine.compute_generation()

            if self.generation%5 == 0: #Send values each three generations
                max_height = 500
                self.H.update_geogrid_data(update_land_uses, grid_list=self.genMachine.population_matrix[0, :], dict_landUses=dict_landUses, height=max_height)

            self.generation +=1
        i = 0

    def on_resume(self):
        while True:
            if generation%5==0:
                print("Press 'c' to continue")
                print("Press 'e' to calibrate the table")
                ch = input("['c','e']>>>")
            
                if ch == "e":
                    break   

            print("Generation : ", generation)

            self.genMachine.compute_generation()

            if generation%5 == 0: #Send values each three generations
                max_height = 500
                self.H.update_geogrid_data(update_land_uses, grid_list=self.genMachine.population_matrix[0, :], dict_landUses=dict_landUses, height=max_height)

            generation +=1


    def on_stop(self):
        print("Now, interact!")



table_name = 'geneticcity'
H = Handler(table_name)

#Initialise the Genetic Machine
genMachine = GeneticMachine()

#Initialise the Main Machine
#mainMachine = MainMachine(genMachine,H)
mainMachine = MainMachine(genMachine)


#Create list to store fitness for different rules
fitness_rules_solutions = []

#Initialise connection to ARUCO server
ip = '127.0.0.1'
port = 15800
# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (ip, port)
s.bind(server_address)

# Starting Ray for parallelization
ray.init()

#START OF GENERATON LOOP ################################################################################################################
mainMachine.start()