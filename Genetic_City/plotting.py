# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import matplotlib
import imageio
import numpy as np
import os
from datetime import datetime
from datetime import date
import glob
from PIL import Image
from parameters import *
import string
from initFunctions import *
import pandas as pd
from math import pi
import json

matplotlib.use('agg')

def load_grid_data(file_loc):
    with open(file_loc) as f:
        lines = f.readlines()
        grid_list = []
    for line in lines:
        grid_list.extend([int(n.split('.')[0]) for n in line.split(',')])
    return grid_list


def grid_plot(plot_size, colormap, path_plotting, path_images):

    for files in os.listdir(path_plotting+'/'):
        f = os.path.join(path_plotting, files)
        if os.path.isfile(f) and files != '.DS_Store':
            grid_list = np.resize(np.asarray(load_grid_data(f)), [
                                  plot_size, plot_size])
            plt.style.use('dark_background')
            Z = grid_list
            x = np.arange(0, plot_size+1, 1)
            y = np.arange(0, plot_size+1, 1)
            fig, ax = plt.subplots()
            pc = ax.pcolormesh(x, y, Z, cmap=colormap, linewidths=2)
            ax.axis('off')
            plt.savefig(path_images+'/'+str(files)+'.png')
            fig.clear()
            plt.close('all')


def fitness_plot(best_outputs, path_images, generation, num_generations, counter2):
    fig, ax = plt.subplots()
    pc = ax.plot(best_outputs)
    # import ipdb
    # ipdb.set_trace()
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Fitness")
    plt.xlim([0, num_generations])
    plt.ylim([0, 100])
    plt.savefig(str(path_images)+'/'+str(dictionary_images[counter2])+'_'+str(
        generation)+'_generation_'+'fitnessOutputs'+'.png')
    fig.clear()
    plt.close('all')

# Function for plotting the Radar Chart with the different rules


def radar_plot(path_images_radar, dictionary_rules_fitness, generation, counter3):
    fig, ax = plt.subplots()
    plt.style.use('classic')
    # import ipdb
    # ipdb.set_trace()
    # number of variable
    categories=list(['accesibility','green space amount','green space width','housing diversity', 
                    'office diversity','walkable house-office','parks access','house office balance','people_fitting'])
    N = len(categories)

    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values = list(dictionary_rules_fitness.values())
    values.append(values[0])

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True, facecolor='k')
    plt.style.use('dark_background')
    
    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, size=8)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([10,20,30,40,50,60,70,80,90], [
        "10","20","30","40","50","60","70","80","90"], size=7)
    plt.ylim(0,100)

    #Change the color of the tick labels
    ax.tick_params(colors='#ffffff')
    
    # Change the color of the circular gridlines.
    ax.grid(color='#ffffff')

    # Change the color of the outermost gridline (the spine).
    ax.spines['polar'].set_color('#ffffff')

    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid', color='w')
    
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Go through labels and adjust alignment based on where
    # it is in the circle.
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    # Save the graph
    plt.savefig(str(path_images_radar)+'/'+str(dictionary_images[counter3])+'_'+str(
        generation)+'_generation_'+'radarPlot'+'.png')
    fig.clear()
    plt.close('all')
    return


def fitnessAndCityPlot(best_outputs, input_city, colormap):
    size = input_city.shape[0]
    plt.style.use('dark_background')
    Z = input_city.reshape((size, size))
    x = np.arange(0, size+1, 1)  # len = 11
    y = np.arange(0, size+1, 1)  # len = 7
    fig, (ax1, ax2) = plt.subplots(1, 2)
    pc1 = ax1.pcolormesh(x, y, Z, cmap=colormap, linewidths=2)
    pc2 = ax2.plot(best_outputs)
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Fitness")
    plt.show()

    return

def saveImages(so_far_blocks, matrix_with_roads_amplified, best_outputs, colormap, generation, path_images_solution, path_images_fitness, path_images_matrix, path_plotting, num_generations, counter1, counter2, counter3, counter4, path_images_radar, dictionary_rules_fitness):
    # Save plotting
    np.savetxt(str(path_plotting)+'\\'+str(dictionary_images[counter1])+'_'+str(
        generation)+'_generation_'+'block_solution_amplified'+'.txt', matrix_with_roads_amplified, delimiter=',')
    # Save blocks
    grid_plot(np.shape(matrix_with_roads_amplified)[
              0], colormap, path_plotting, path_images_solution)
    fitness_plot(best_outputs, path_images_fitness,
                 generation, num_generations, counter2)
    radar_plot(path_images_radar, dictionary_rules_fitness,
               generation, counter3)
    output_obj = {'block': matrix_with_roads_amplified.tolist(),
                  'fitness': best_outputs, 'radar': dictionary_rules_fitness}
    log_path = str(path_plotting)+'\\log\\' + \
        str(dictionary_images[counter1])+'_'+str(generation)+'_generation.json'
    with open(log_path, "w") as f:
        json.dump(output_obj, f, sort_keys=True, separators=(',', ':'))


def create_directory_images():
    time = datetime.now()
    current_time = time.strftime("%H.%M.%S")
    day = date.today()
    current_day = day.strftime("%b_%d_%Y")
    directory = current_day + "_" + current_time
    print("The directory where files were saved is: "+directory)
    # Define parent directory
    parent_dir = os.path.join(path_to_code, "results")
    # Define complete path
    path = os.path.join(parent_dir, directory)
    # Create the directory
    os.mkdir(path)

    # Define images path
    path_images = os.path.join(path, "images")
    # Define plotting path
    path_plotting = os.path.join(path, "plotting")
    #Define log path
    path_log = os.path.join(path_plotting, "log")
    # Create directories for images and plotting
    os.mkdir(path_images)
    os.mkdir(path_plotting)
    os.mkdir(path_log)
    # Define the path for solution
    path_images_solution = os.path.join(path_images, "solution")
    # Define the path for fitness
    path_images_fitness = os.path.join(path_images, "fitness")
    # Define the path for radar
    path_images_radar = os.path.join(path_images, "radar")
    #Define the path for matrix
    path_images_matrix = os.path.join(path_images, "matrix")
    # Define the path for GIF
    path_images_GIF = os.path.join(path_images, "gif")
    # Create the directory for solution, fitness function, radar and GIF
    os.mkdir(path_images_solution)
    os.mkdir(path_images_fitness)
    os.mkdir(path_images_radar)
    os.mkdir(path_images_GIF)
    os.mkdir(path_images_matrix)

    return path, path_images_solution, path_images_fitness, path_images_radar, path_images_GIF, path_plotting, path_images_matrix


def create_gifs(frame_folder):
    frames = [Image.open(image)
              for image in glob.glob(f"{frame_folder}/*.png")]
    frame_one = frames[0]
    frame_one.save(frame_folder+"/my_awesome.gif", format="GIF", append_images=frames,
                   save_all=True, duration=time_per_image, loop=0)


# Function for concatenating images or gifs and saving them in the provided folder
def get_concat_h(im1_path, im2_path, im3_path, folder):
    frames_solution = [Image.open(image) for image in sorted(
        glob.glob(f"{im1_path}/*.png"))]
    frames_fitness = [Image.open(image)
                      for image in sorted(glob.glob(f"{im2_path}/*.png"))]
    frames_radar = [Image.open(image)
                    for image in sorted(glob.glob(f"{im3_path}/*.png"))]
    for i in np.arange(len(frames_solution)):
        im1 = frames_solution[i]
        im2 = frames_fitness[i]
        im3 = frames_radar[i]
        dst = Image.new('RGB', (im1.width + im2.width + im3.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        dst.paste(im3, (im1.width+im2.width, 0))
        dst.save(folder+'/concatenated'+str(i)+'.png')
    return
