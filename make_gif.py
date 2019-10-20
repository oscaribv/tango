#---------------------------------------------------------------
#       TANGO: Transit ANimation for General Orbits 
#             October 2018, Oscar Barragan
#---------------------------------------------------------------

#Load libraries
import sys
import os
from matplotlib import gridspec
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks')
sns.set_color_codes()

#Start TANGO as ./tango.py system
system = str(sys.argv[1])

exec(open('src/default.py').read())

exec(open(system+'/input.py').read())


#---------------------------------------------------------------
#                      END plot creation
#---------------------------------------------------------------
#                    Start  movie creation
#---------------------------------------------------------------

exec(open('src/moviepy_src.py').read())

#---------------------------------------------------------------
#                    End movie creation
#---------------------------------------------------------------
