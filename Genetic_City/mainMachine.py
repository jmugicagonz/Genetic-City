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
import socket                                                                   #Library to read from server
import random

class MainMachine(StateMachine):
    #Defining states and transitions
    initialized = State('Initialized', initial=True)
    computing_generations = State('Computing')
    calibrating = State('Calibrating')
    user_interacting = State('Interacting')

    start = initialized.to(computing_generations)
    calibrate = computing_generations.to(calibrating)
    interact = calibrating.to(user_interacting)
    resume = user_interacting.to(computing_generations)

    #Initialise the Genetic Machine
    genMachine = GeneticMachine()

    #Initialise connection to cityIO
    table_name = 'geneticcity8'
    H = Handler(table_name)

    generation = 0 #Represents a counter to know how many generations have been computed

    #Initialise connection to ARUCO server
    ip = '127.0.0.1'
    port = 15800
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
    server_address = (ip, port)
    s.bind(server_address) # Bind the socket to the port

    def on_start(self):
        print("STARTING GENETIC ALGORITHM")
        while True:
            print("Generation : ", self.generation)
            self.genMachine.compute_generation()
            if self.generation%5 == 0: #Send values each three generations
                max_height = int((self.generation+1)*2)
                if max_height>500: max_height=500
                landUses_to_send = self.genMachine.population_matrix[0, :]
                self.grid_to_send = [(0,0) for _ in np.arange(len(landUses_to_send))]
                for i in np.arange(len(landUses_to_send)):
                    randomTall = random.uniform(0,1)
                    randomH = random.randint(0,max_height)
                    if landUses_to_send[i] == 2: 
                        if randomTall >= 0.9: height = 4*randomH
                        elif randomTall >= 0.5: height = 2*randomH
                        else: height = randomH
                    elif landUses_to_send[i] == 3: 
                        if randomTall >= 0.8: height = 2*randomH
                        elif randomTall >= 0.5: height = randomH
                        else: height = int(0.5*randomH)
                    elif landUses_to_send[i] == 1: height = 0
                    self.grid_to_send[i] = (landUses_to_send[i],height)
                self.H.update_geogrid_data(update_land_uses, grid_list= self.grid_to_send, dict_landUses=dict_landUses)
                print("Press intro to continue")
                print("Press 'e' to go and calibrate the table")
                ch = input("['c','e']>>>")
                if ch == "e":
                    break 
            self.generation +=1
        i = 0

    def on_calibrate(self):
        print("Table automatic calibration. If blocked, try to move swap two pieces")
        ch = "c"
        while True:
            if ch == "c":
                print("Please move two pieces to let the system calibrate")
                data1, address = self.s.recvfrom(4096)
                data2 = data1.decode("utf-8")
                ids_p = [int(id) for id in data2.split(' ')[1:-1]]
                ids = [0]*len(ids_p)
                set_recheck = set(np.arange(len(ids_p)))
                while(len(set_recheck)>0):
                    i = set_recheck.pop()
                    if ids_p[i]!=-1:
                        ids[i] = ids_p[i]
                    else:
                        set_recheck.add(i)
                        data1, address = self.s.recvfrom(4096)
                        data2 = data1.decode("utf-8")
                        ids_p = [int(id) for id in data2.split(' ')[1:-1]]
                print("Calibration completed. Press 'e' to stop calibration and go interacting")
                ch = input("['c','e']>>>")
            elif ch == "e":
                break

        print("Ids selected are: {}".format(ids))
        self.ids = ids.copy()
        self.idsUsesHeights = dict()
        for i in range(len(self.ids)):
            self.idsUsesHeights[ids[i]] = self.grid_to_send[i]
        print("Ids uses are: {}".format(self.idsUsesHeights))

    def on_interact(self):
        while True:
            print("Please interact with the table and type 'c' to send interaction")
            #print("Press 'e' to exit")
            #ch = input("['c','e']>>>")
            #if ch == "c":
            considered_changes = set()
            ids = dict()
            while(len(considered_changes)<2):
                data1, address = self.s.recvfrom(4096)
                data2 = data1.decode("utf-8")
                ids_p = [int(id) for id in data2.split(' ')[1:-1]]
                for i in np.arange(len(ids_p)):
                    if ids_p[i]!=-1 and ids_p[i]!=self.ids[i] and (ids_p[i] in self.idsUsesHeights) and (i not in considered_changes):
                        print("Change counter increased")
                        print("Triggering id is: {}".format(ids_p[i]))
                        print("Original id is: {}".format(self.ids[i]))
                        ids[i] = ids_p[i]
                        considered_changes.add(i)
            print("Ids selected are: {}".format(ids))
            for element in ids:
                self.ids[element] = ids[element]
            print("Ids to be sent are: {}".format(ids))
            "You send a new vector with land uses to the cityIO"
            self.grid_to_send = []
            for i in range(len(self.ids)):
                    landUse = self.idsUsesHeights[self.ids[i]][0]
                    height = self.idsUsesHeights[self.ids[i]][1]
                    self.grid_to_send.append((landUse, height))
            print("Land uses and heights to send is: {}".format(self.grid_to_send))
            self.H.update_geogrid_data(update_land_uses, grid_list=self.grid_to_send, dict_landUses=dict_landUses)
            '''elif ch == "e":
                break  '''  

    def on_resume(self):
        print("Starting the genetic algorithm")
        while True:
            if generation%5==0:
                print("Press 'c' to continue and calculate more generations")
                print("Press 'e' to exit and go calibrate the table")
                ch = input("['c','e']>>>")
            
                if ch == "e":
                    break   

            print("Generation : ", generation)

            self.genMachine.compute_generation()

            if generation%5 == 0: #Send values each three generations
                max_height = 500
                self.H.update_geogrid_data(update_land_uses, grid_list=self.genMachine.population_matrix[0, :], dict_landUses=dict_landUses, height=max_height)

            generation +=1