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
import cv2
import numpy as np
import glob
import re

img_array = []
files =glob.glob('C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City/results/Mar_10_2022_20.35.30/matrix/*.JPEG')
files.sort()
# if you want sort files according to the digits included in the filename, you can do as following:

for filename in files:
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('matrix.avi',cv2.VideoWriter_fourcc(*'DIVX'), 40, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()


'''def create_gifs(frame_folder):
    frames = [Image.open(image)
              for image in glob.glob(f"{frame_folder}/*.png")]
    frame_one = frames[0]
    frame_one.save(frame_folder+"/my_awesome.gif", format="GIF", append_images=frames,
                   save_all=True, duration=100, loop=0)

create_gifs('C:/Users/adminlocal/Documents/WorkspacesPython/Genetic-City/Genetic_City/results/Mar_10_2022_19.56.39/images/radar')'''