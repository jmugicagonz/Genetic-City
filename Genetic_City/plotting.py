import matplotlib.pyplot as plt
import numpy as np
import os


def load_grid_data(file_loc):
    with open(file_loc) as f:
        lines = f.readlines()
        grid_list=[]
    for line in lines:
        grid_list.extend([int(n.split('.')[0]) for n in line.split(',')])
    return grid_list


def grid_plot(plot_size, colormap):
    directory = 'C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City/plotting/'

    for files in os.listdir(directory):
        f = os.path.join(directory, files)
        if os.path.isfile(f) and files != '.DS_Store':
            
            grid_list=np.resize(np.asarray(load_grid_data(f)),[plot_size,plot_size])
            plt.style.use('dark_background')
            Z = grid_list
            x = np.arange(0, plot_size+1, 1)
            y = np.arange(0, plot_size+1, 1)
            fig, ax = plt.subplots()
            pc = ax.pcolormesh(x, y, Z, cmap=colormap,linewidths=2)
            ax.axis('off')
            plt.savefig('C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City/images/'+str(files)+'.png')

def fitness_plot(best_outputs):
    fig, ax = plt.subplots()
    pc = ax.plot(best_outputs)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Fitness")
    plt.savefig('C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City/images/'+'fitnessOutputs'+'.png')

def fitnessAndCityPlot (best_outputs,input_city, colormap):
    size = input_city.shape[0]
    plt.style.use('dark_background')
    Z = input_city.reshape((size, size))
    x = np.arange(0, size+1, 1)  # len = 11
    y = np.arange(0, size+1, 1)  # len = 7
    fig, (ax1, ax2) = plt.subplots(1,2)
    '''for i in range(grid_size+1):
        #We define each line to be plotted with its line's
        ax.plot(np.arange(size+1), np.repeat(i*block_size,size+1), linewidth = '5', color = 'gray')
        ax.plot(np.repeat(i*block_size,size+1), np.arange(size+1),  linewidth = '5', color = 'gray')'''
    #print("Z to show in colormesh") 
    #print(Z)
    pc1 = ax1.pcolormesh(x, y, Z, cmap=colormap,linewidths=2)
    pc2 = ax2.plot(best_outputs)
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Fitness")
    #ax2.axis('off')
    #fig.colorbar(pc, ax)
    plt.show()

    return