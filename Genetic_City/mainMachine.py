from statemachine import StateMachine, State
import keyboard                                                                 #Library for stopping the code when pressing a letter                                                            
import numpy as np                                                              #Matrix and array handling.
import matplotlib.pyplot as plt                                                 #Plotting

import threading                                                                # Library to run multiple threads
import time
import keyboard                                                                 #Library for stopping the code when pressing a letter
import ray
import socket                                                                   #Library to read from server


from plotting import *                                                          #Functions for plotting
#from fitnessFunctions import fitness_func
from onlineGrid import *                                                        #Import functions to support online grid
from parameters import *
from geneticMachine import *

import music


class MainMachine(StateMachine):
    #Defining states
    initialized = State('Initialized', initial=True)
    computing_generations = State('Computing')
    calibrating = State('Calibrating')
    user_interacting = State('Interacting')

    #Defining transitions
    start = initialized.to(computing_generations)
    calibrate = computing_generations.to(calibrating)
    interact = calibrating.to(user_interacting)
    resume_genetic = user_interacting.to(computing_generations)
    resume_calibrate = computing_generations.to(calibrating)
    resume_interaction = calibrating.to(user_interacting)

    #Initialise the Genetic Machine
    genMachine = GeneticMachine()
    #Define boolean to play/pause the Genetic Machine
    bool_continue_GM = False
    bool_prev_state = False

    #Initialise connection to cityIO for TV
    table_name = 'geneticcity7'
    H = Handler(table_name)

    # Initialise connection to cityIO for projection
    table_name_projection = 'geneticcity7h0'
    H_projection = Handler(table_name_projection)

    generation = 0 #Represents a counter to know how many generations have been computed

    #Initialise connection to ARUCO server
    ip = '127.0.0.1'
    port = 15800
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
    server_address = (ip, port)
    s.bind(server_address) # Bind the socket to the port

    #Define mask for ids not to be modified
    mask = [0]*(block_size*block_size)

    def read_aruco_check_play_pause(self):
        while not keyboard.is_pressed('t'):    
            self.data1, address = self.s.recvfrom(4096)
            data2 = self.data1.decode("utf-8")
            ids_p = [int(id) for id in data2.split(' ')[1:-1]]
            if ids_p[pos_play_pause] == -1:
                print("Id play pause equal to -1")
                '''data1, address = self.s.recvfrom(4096)
                data2 = data1.decode("utf-8")
                ids_p = [int(id) for id in data2.split(' ')[1:-1]]'''
            if ids_p[pos_play_pause] == id_play:
                if self.bool_prev_state == False:
                    print("Continuing algorithm")
                    self.bool_prev_state = True
                self.continue_GM()
            if ids_p[pos_play_pause] == id_pause:
                if self.bool_prev_state == True:
                    print("Pausing algorithm")
                    self.bool_prev_state = False
                self.pause_GM()

    def on_start(self):
        # Initialise thread in parallel to read from ARUCO
        # Create a Thread with a function without any arguments
        self.th = threading.Thread(target=self.read_aruco_check_play_pause)
        # Start the thread
        self.th.start()
        print("WHENEVER YOU ARE READY, PLAY THE GENETIC ALGORITHM")
        while not self.bool_continue_GM:
            print("Waiting to start. Replace the pause button by the play")
            time.sleep(1)
        print("STARTING GENETIC ALGORITHM")
        music.play_music()
        #while not keyboard.is_pressed('e'):
        while self.bool_continue_GM:
            print("Generation : ", self.generation)
            self.genMachine.compute_generation()
            if self.generation%5 == 0: #Send values each five generations
                max_height = int((self.generation+1)*2)
                if max_height>500: max_height=500
                landUses_to_send = self.genMachine.population_matrix[0, :]
                indicators_to_send = self.genMachine.list_of_dictionaries_rules[0]
                print("Indicators to send are: {}".format(indicators_to_send))
                self.grid_to_send = [(0,0) for _ in np.arange(len(landUses_to_send))]
                self.grid_to_send_projection = [(0,0) for _ in np.arange(len(landUses_to_send))]
                for i in np.arange(len(landUses_to_send)):
                    randomTall = np.random.uniform(0.0,1.0)
                    randomH = np.random.randint(0.0,float(max_height))
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
                    self.grid_to_send_projection[i] = (landUses_to_send[i],0)
                self.H.update_geogrid_data(update_land_uses, grid_list= self.grid_to_send, dict_landUses=dict_landUses)
                self.H_projection.update_geogrid_data(update_land_uses, grid_list= self.grid_to_send_projection, dict_landUses=dict_landUses)
                post_indicators(self.table_name, indicators_to_send)
            self.generation +=1
        self.generation +=1
        music.pause_music()
        #i = 0

    def on_calibrate(self):
        print("STARTING CALIBRATION")
        print("Calibration should be automatic. If blocked, try to move swap two pieces")
        #data1, address = self.s.recvfrom(4096)
        data2 = self.data1.decode("utf-8")
        ids_p = [int(id) for id in data2.split(' ')[1:-1]]
        ids_p = ids_p[0:block_size*block_size]
        ids = [0]*len(ids_p)
        set_recheck = set(np.arange(len(ids_p)))
        while(len(set_recheck)>0):
            i = set_recheck.pop()
            if ids_p[i]!=-1:
                ids[i] = ids_p[i]
            else:
                set_recheck.add(i)
                #data1, address = self.s.recvfrom(4096)
                data2 = self.data1.decode("utf-8")
                ids_p = [int(id) for id in data2.split(' ')[1:-1]]
                ids_p = ids_p[0:block_size*block_size]
        print("Calibration completed.")
        print("Ids selected are: {}".format(ids))
        self.ids = ids.copy()
        self.idsUsesHeights = dict()
        for i in range(len(self.ids)):
            self.idsUsesHeights[ids[i]] = self.grid_to_send[i]
        print("Ids uses are: {}".format(self.idsUsesHeights))

    def on_interact(self):
        print("STARTING INTERACTION")
        while not self.bool_continue_GM:
            print("Please interact with the table")
            considered_changes = set()
            ids = dict()
            #while(len(considered_changes)<2):
            data2 = self.data1.decode("utf-8")
            ids_p = [int(id) for id in data2.split(' ')[1:-1]]
            ids_p = ids_p[0:block_size*block_size]
            for i in np.arange(len(ids_p)):
                if ids_p[i]!=-1 and ids_p[i]!=self.ids[i] and (ids_p[i] in self.idsUsesHeights): # and (i not in considered_changes): TODO: eliminate this comment asap
                    print("Change counter increased")
                    print("Triggering id is: {}".format(ids_p[i]))
                    print("Original id is: {}".format(self.ids[i]))
                    ids[i] = ids_p[i]
                    # considered_changes.add(i)
            if self.bool_continue_GM: break
            print("Ids selected are: {}".format(ids))
            for element in ids:
                self.ids[element] = ids[element]
            print("Ids to be sent are: {}".format(ids))
            "You send a new vector with land uses to the cityIO"
            self.grid_to_send = []
            self.grid_to_send_projection = []
            self.land_uses_from_interaction = []
            for i in range(len(self.ids)):
                    landUse = self.idsUsesHeights[self.ids[i]][0]
                    height = self.idsUsesHeights[self.ids[i]][1]
                    self.grid_to_send.append((landUse, height))
                    self.grid_to_send_projection.append((landUse,0))
                    self.land_uses_from_interaction.append(landUse)
            print("Land uses and heights to send is: {}".format(self.grid_to_send))
            _, new_dictionary_rules_fitness = fitness_func(np.asarray(self.land_uses_from_interaction), create_set_rules(), self.genMachine.weights) #TODO: modify to centralize parameters
            post_indicators(self.table_name, new_dictionary_rules_fitness)
            self.H.update_geogrid_data(update_land_uses, grid_list=self.grid_to_send, dict_landUses=dict_landUses)
            self.H_projection.update_geogrid_data(update_land_uses, grid_list=self.grid_to_send_projection, dict_landUses=dict_landUses)
        print("EXITING INTERACTION")

    def on_resume_genetic(self):
        print("RESUMING THE GENETIC ALGORITHM")
        music.resume_music()
        self.genMachine.continue_generation(self.land_uses_from_interaction)
        while self.bool_continue_GM:
            print("Generation : ", self.generation)
            self.genMachine.compute_generation()
            if self.generation%5 == 0: # Send values each five generations
                max_height = int((self.generation+1)*2)
                if max_height>500: max_height=500
                landUses_to_send = self.genMachine.population_matrix[0, :]
                indicators_to_send = self.genMachine.list_of_dictionaries_rules[0]
                print("Indicators to send are: {}".format(indicators_to_send))
                #self.grid_to_send = [(0,0) for _ in np.arange(len(landUses_to_send))]
                for i in np.arange(len(landUses_to_send)):
                    randomTall = np.random.uniform(0.0,1.0)
                    randomH = np.random.randint(0.0,float(max_height))
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
                    self.grid_to_send_projection[i] = (landUses_to_send[i],0)
                self.H.update_geogrid_data(update_land_uses, grid_list= self.grid_to_send, dict_landUses=dict_landUses)
                self.H_projection.update_geogrid_data(update_land_uses, grid_list= self.grid_to_send_projection, dict_landUses=dict_landUses)
                post_indicators(self.table_name, indicators_to_send)
            self.generation +=1
        self.generation +=1
        music.pause_music()

    def on_resume_calibrate(self):
        print("STARTING CALIBRATION")
        print("Calibration should be automatic. If blocked, try to move swap two pieces")
        #data1, address = self.s.recvfrom(4096)
        data2 = self.data1.decode("utf-8")
        ids_p = [int(id) for id in data2.split(' ')[1:-1]]
        ids_p = ids_p[0:block_size*block_size]
        ids = [0]*len(ids_p)
        set_recheck = set(np.arange(len(ids_p)))
        while(len(set_recheck)>0):
            i = set_recheck.pop()
            if ids_p[i]!=-1:
                ids[i] = ids_p[i]
            else:
                set_recheck.add(i)
                #data1, address = self.s.recvfrom(4096)
                data2 = self.data1.decode("utf-8")
                ids_p = [int(id) for id in data2.split(' ')[1:-1]]
                ids_p = ids_p[0:block_size*block_size]
        print("Calibration completed.")
        print("Ids selected are: {}".format(ids))
        self.ids = ids.copy()
        self.idsUsesHeights = dict()
        for i in range(len(self.ids)):
            self.idsUsesHeights[ids[i]] = self.grid_to_send[i]
        print("Ids uses are: {}".format(self.idsUsesHeights))

    def on_resume_interaction(self):
        print("STARTING INTERACTION")
        #while not keyboard.is_pressed('e'):
        while not self.bool_continue_GM:
            print("Please interact with the table")
            considered_changes = set()
            ids = dict()
            while(len(considered_changes)<2):
                data2 = self.data1.decode("utf-8")
                ids_p = [int(id) for id in data2.split(' ')[1:-1]]
                ids_p = ids_p[0:block_size*block_size]
                for i in np.arange(len(ids_p)):
                    if ids_p[i]!=-1 and ids_p[i]!=self.ids[i] and (ids_p[i] in self.idsUsesHeights) and (i not in considered_changes):
                        print("Change counter increased")
                        print("Triggering id is: {}".format(ids_p[i]))
                        print("Original id is: {}".format(self.ids[i]))
                        ids[i] = ids_p[i]
                        considered_changes.add(i)
                if self.bool_continue_GM: break
            print("Ids selected are: {}".format(ids))
            for element in ids:
                self.ids[element] = ids[element]
            print("Ids to be sent are: {}".format(ids))
            "You send a new vector with land uses to the cityIO"
            self.grid_to_send = []
            self.grid_to_send_projection = []
            self.land_uses_from_interaction = []
            for i in range(len(self.ids)):
                    landUse = self.idsUsesHeights[self.ids[i]][0]
                    height = self.idsUsesHeights[self.ids[i]][1]
                    self.grid_to_send.append((landUse, height))
                    self.grid_to_send_projection.append((landUse,0))
                    self.land_uses_from_interaction.append(landUse)
            print("Land uses and heights to send is: {}".format(self.grid_to_send))
            _, new_dictionary_rules_fitness = fitness_func(np.asarray(self.land_uses_from_interaction), create_set_rules(), self.genMachine.weights) #TODO: modify to centralize parameters
            post_indicators(self.table_name, new_dictionary_rules_fitness)
            self.H.update_geogrid_data(update_land_uses, grid_list=self.grid_to_send, dict_landUses=dict_landUses)
            self.H_projection.update_geogrid_data(update_land_uses, grid_list=self.grid_to_send_projection, dict_landUses=dict_landUses)
            '''print("Press intro to continue or 'e' to continue running the genetic algorithm")
            ch = input("['Intro','e']>>>")
            if ch == "e":
                break '''
    

    def continue_GM(self):
        self.bool_continue_GM = True

    def pause_GM(self):
        self.bool_continue_GM = False
