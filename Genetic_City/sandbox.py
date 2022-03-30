import numpy as np
from brix import Handler                                                        #Module to communicate with the CityIO
import random                                                                   #Used to send random heights of buildings
import socket
import sys


list1 = [0,1,2,3]
list2 = list1
list2[2] = 7
print(list1)