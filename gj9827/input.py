#Input file for tango
#system: GJ 9827
#Created by O. Barragan, October 2018.

#Data file with the flattened light curve
lcname = 'lc_gj9827.dat'

#--------------------------------------------------------------------
#                 Planet and orbit parameters
# Each parameter is a list in which each element
# correspond to a planet. For this case, there are three
# planets. But you can create animations with 1, 2, 3, and more planets.
#--------------------------------------------------------------------

#This file was creating using the values reported in Prieto-Arranz et al., (2018)
#Orbital period (days)
P =[1.2089662,3.6482269,6.2014190]
#time of mid-transit (days) Be sure that you are using the same units that in your data file
T0 = [2905.8264631,2905.5496113,2907.9619764]
#Orbit eccentricity
e = [0.,0.,0.]
#Angle of periastron
w = [np.pi/2,np.pi/2,np.pi/2]
#Scaled semi-major axis
a = [7.229235,15.096,21.5019118]
#orbit inclination (degrees)
inclination = [88.330714*np.pi/180,89.06*np.pi/180,87.702*np.pi/180]
#Scaled planet radius (Rp/R*)
rp = [0.0232259,0.0181983,0.0299279]
#Limb darkening coefficients following a quadratic law
u1 =  0.58
u2 =  0.15
#Next two variables are used to control the cadence of the light curve data
#Integration time of the data
t_cad = 30./60./24.
#Number of steps to integrate the data
n_cad = 10
#These values are useful now to integrate Kepler long cadence data

#The code can estimate the stellar colour based on Halle & Heller 2021
#Assuming is a black body given a stellar temperature T_star in Kelvin
T_star = 4200 #K


#--------------------------------------------------------------------
#              Animation controls
#--------------------------------------------------------------------
#Window size to show the data (days)
size_time = 0.5 
#1./(photograms per day) in this case the code will create a photogram each 7.2 min
vel_time  = 1./500.
#Animation minimum time (Be sure that you are using the same units as in your data file)
tmin =  2963.3
#Animation maximum time (Be sure that you are using the same units as in your data file)
tmax =  2964.3
#frame rate
frate = 1./24.

#--------------------------------------------------------------------
#                     Plot controls
#--------------------------------------------------------------------

#Control if we overplot the light curve model
#You need to have installed pyaneti in your computer to use it
is_plot_model = False

#-----------------------------------------------------------------
#                         END
#-----------------------------------------------------------------
