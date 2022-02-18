import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
from datetime import date
import glob
from PIL import Image
from parameters import *
import string



def load_grid_data(file_loc):
    with open(file_loc) as f:
        lines = f.readlines()
        grid_list=[]
    for line in lines:
        grid_list.extend([int(n.split('.')[0]) for n in line.split(',')])
    return grid_list


def grid_plot(plot_size, colormap, path_plotting, path_images):

    for files in os.listdir(path_plotting+'/'):
        f = os.path.join(path_plotting, files)
        if os.path.isfile(f) and files != '.DS_Store':         
            grid_list=np.resize(np.asarray(load_grid_data(f)),[plot_size,plot_size])
            plt.style.use('dark_background')
            Z = grid_list
            x = np.arange(0, plot_size+1, 1)
            y = np.arange(0, plot_size+1, 1)
            fig, ax = plt.subplots()
            pc = ax.pcolormesh(x, y, Z, cmap=colormap,linewidths=2)
            ax.axis('off')
            plt.savefig(path_images+'/'+str(files)+'.png')

def fitness_plot(best_outputs,path_images,generation,num_generations, counter2):
    fig, ax = plt.subplots()
    pc = ax.plot(best_outputs)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Fitness")
    plt.xlim([0, num_generations])
    plt.savefig(path_images+'/'+dict[counter2]+'_'+str(generation)+'_generation_'+'fitnessOutputs'+'.png')

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

def saveImages (matrix_with_roads_amplified, best_outputs, colormap, generation, path_images_solution,path_images_fitness, path_plotting, num_generations, counter1, counter2):
    #Save plotting
    np.savetxt(path_plotting+'/'+dict[counter1]+'_'+str(generation)+'_generation_'+'block_solution_amplified'+'.txt',matrix_with_roads_amplified,delimiter=',')
    #Save blocks
    grid_plot(np.shape(matrix_with_roads_amplified)[0], colormap, path_plotting, path_images_solution)
    fitness_plot(best_outputs, path_images_fitness, generation, num_generations, counter2)

def create_directory_images():
    time = datetime.now()
    current_time = time.strftime("%H.%M.%S")
    day = date.today()
    current_day = day.strftime("%b_%d_%Y")
    directory = current_day + "_" + current_time
    print("The directory where files were saved is: "+directory)
    #Define parent directory
    parent_dir = "C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City/results/"
    #Define complete path
    path = os.path.join(parent_dir, directory)
    #Create the directory
    os.mkdir(path)
    #Define images path
    path_images = os.path.join(path, "images")
    #Define plotting path
    path_plotting = os.path.join(path, "plotting")
    #Create directories for images and plotting
    os.mkdir(path_images)
    os.mkdir(path_plotting)
    #Define the path for solution
    path_images_solution = os.path.join(path_images,"solution")
    #Define the path for fitness
    path_images_fitness = os.path.join(path_images,"fitness")
    #Define the path for GIF
    path_images_GIF = os.path.join(path_images,"gif")
    #Create the directory for solution, fitness function and GIF
    os.mkdir(path_images_solution)
    os.mkdir(path_images_fitness)
    os.mkdir(path_images_GIF)

    return path_images_solution, path_images_fitness, path_images_GIF, path_plotting


def create_gifs(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    frame_one = frames[0]
    frame_one.save(frame_folder+"/my_awesome.gif", format="GIF", append_images=frames,
               save_all=True, duration=time_per_image, loop=0)


#Function for concatenating images or gifs and saving them in the provided folder
def get_concat_h(im1_path, im2_path, folder):
    frames_solution = [Image.open(image) for image in sorted(glob.glob(f"{im1_path}/*.png"))]
    frames_fitness = [Image.open(image) for image in sorted(glob.glob(f"{im2_path}/*.png"))]
    for i in np.arange(len(frames_solution)):
        im1 = frames_solution[i]
        im2 = frames_fitness[i]
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        dst.save(folder+'/concatenated'+str(i)+'.png')
    return