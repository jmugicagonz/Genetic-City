import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import Counter
import pygad
import json

""" GRID AND GRAPH """

class Grid:
    """
    The grid of land-use types
    Initialised by the output of the 1st GA
    """
    def __init__(self, rows, cols, grid_types):
        self.rows=rows
        self.cols=cols
        self.grid_types=grid_types
        
    def generate_dist_mat(self):
        source_i_2d=[[i]*self.cols for i in range(self.rows)]
        source_i=[j for sub in source_i_2d for j in sub]
        source_j=list(range(self.cols))*self.rows
        
        manhattan_distmat=np.array([[np.abs(source_i[ind]-i)+np.abs(source_j[ind]-j) for i in range(rows) for j in range(cols)
                           ] for ind in range(len(source_i))])
        return manhattan_distmat
        
        
    def generate_od(self, source_id, dest_id, power=1):
        origin_mask=(np.array(self.grid_types)==source_id).astype(int)
        # print("Origin mask: ")
        # print(origin_mask)
        destination_mask=(np.array(self.grid_types)==dest_id).astype(int)
        # print("Destination mask: ")
        # print(destination_mask)
        manhattan_distmat=self.generate_dist_mat()
        # print("Manhattan dist mat: ")
        # print(manhattan_distmat)
        
        od=1/np.power(manhattan_distmat, power) # initialise OD as inverse of friction function
        # print("Od initialization: ")
        # print(od)
        od=np.multiply(od, destination_mask) # non-dest cols to zero
        # print("Od after non-dest columns to zero")
        # print(od)
        od=np.multiply(od.T, origin_mask).T # non-source rows to zero
        # print("Od after non source rows to zero: ")
        # print(od)
        
        od=np.nan_to_num(od, nan=0, posinf=0) # Convert inf (trips with zero friction. i.e. to and from same cell) to zero
        # print("Od after conv inf to zero: ")
        # print(od)
        
        # Furness method
        for i in range(10):
            sum_each_col=od.sum(axis=0)
            sum_each_col[sum_each_col==0]=1 # to avoid division by zero error- multiplying zero by 1 wont make a difference anyway
            od=np.multiply(od, 1/sum_each_col)

            sum_each_row=od.sum(axis=1)
            sum_each_row[sum_each_row==0]=1
            od=np.multiply(od.T, 1/sum_each_row).T
            # print(od[np.where(od!=0)])            
        return od
        
    def plot_grid(self, colors):
        plt.figure(figsize=(12,12))
        cell_cols=[colors[c] for c in self.grid_types]
        X=[ind%cols for ind in range(len(self.grid_types))]
        Y=[int(ind/cols)for ind in range(len(self.grid_types))]
        plt.scatter(X, Y, color=cell_cols, marker='s', s=1300)

        
class GridGraph():
    """
    The road network joining the grid cells
    """
    def __init__(self, rows, cols,  fixed_time_costs, distance_costs, modes):
        #Create a grah with the number of rows and columns
        G=nx.grid_graph([rows, cols])
        #Asign a number for each node corresponding to the number in the reshaped to a single array
        node_name_dict={g: g[0]*cols+g[1] for g in list(G.nodes)}
        G = nx.relabel_nodes(G, node_name_dict)
        self.edge_list=list(G.edges)
        self.G=G
        self.fixed_time_costs=fixed_time_costs
        self.distance_costs=distance_costs
        self.modes=modes
        
    def set_edge_types(self, edge_types, type_to_attributes):
        self.edge_types=edge_types
        # print("Edge types: ")
        # print(self.edge_types)
        edge_attributes={e:type_to_attributes[edge_types[i_e]] for i_e, e in enumerate(self.edge_list)}
        # print("Edge attributes: ")
        # print(edge_attributes)
        nx.set_edge_attributes(self.G, edge_attributes)
        self.get_all_routes()
        
    def get_all_routes(self):
        """
        For a given road network, precompute the shorest paths between every pair of nodes
        Do this separately for each mode
        """
        self.fw_by_mode={}
        for mode in self.modes:
            pred, dist=nx.floyd_warshall_predecessor_and_distance(self.G, weight=mode)
            self.fw_by_mode[mode]={'pred': pred, 'dist': dist}
            print("Self.fw_by_mode: ")
            print(self.fw_by_mode)
            
    def plot_by_type(self, type_colors):
        plt.figure(figsize=(10,10))
        for ie, e in enumerate(self.edge_list):
            from_node, to_node=e[0], e[1]
            e_type=self.edge_types[ie]
            from_x, from_y= from_node%cols, int(from_node/cols)
            to_x, to_y= to_node%cols, int(to_node/cols)
            plt.plot([from_x, to_x], [from_y, to_y], color=type_colors[e_type])
            
    def get_all_path_lengths(self, source, dest):
        """
        For a given source and destination node, get the paths lengths by each mode, including fixed time costs
        """
        all_mode_path_lengths={}
        for mode in self.fw_by_mode:
            all_mode_path_lengths[mode]=self.fw_by_mode[mode]['dist'][source][dest]+self.fixed_time_costs[mode]
        return all_mode_path_lengths
            
    def get_edge_path(self, source, dest, mode):
        """
        get the path taken from a origin node to a destination node for a particular mode
        """
        pred=self.fw_by_mode[mode]['pred']
        path=nx.algorithms.shortest_paths.dense.reconstruct_path(source, dest, pred)
        edge_path=[]
        for i in range(len(path)-1):
            try:
                edge=self.edge_list.index((path[i], path[i+1]))
            except:
                edge=self.edge_list.index((path[i+1], path[i]))
            edge_path.append(edge)
        return edge_path
            
    def assign_traffic(self, od):
        """
        For a given O-D matrix and road network, compute the traffic on the road network
        """
        traffic={mode: {e:0 for e in range(len(self.edge_list))} for mode in self.modes}
        total_cost=0
        for o in range(od.shape[0]):
        #     print(o)
            for d in range(od.shape[1]):
                if not o==d:
                    N=od[o,d]
                    all_mode_path_lengths=self.get_all_path_lengths(o, d)
                    mode=max(all_mode_path_lengths, key=all_mode_path_lengths.get)
                    travel_time_cost=all_mode_path_lengths[mode]
                    path=self.get_edge_path(o, d, mode)
                    dist_cost=self.distance_costs[mode]*len(path)
                    total_cost+=(dist_cost+travel_time_cost)
                    for l in path:
                        traffic[mode][l]+=N 
        return traffic, total_cost

rows=12
cols=12
colors=['white', 'purple', 'green', 'red']

""" GENERATE GRID AND OD """
def load_grid_data(file_loc):
    with open(file_loc) as f:
        lines = f.readlines()
    grid_list=[]
    for line in lines:
        grid_list.extend([int(n.split('.')[0]) for n in line.split(',')])  
    return grid_list

grid_list=load_grid_data('city_mambers1.txt')
