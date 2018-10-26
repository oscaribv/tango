#Default file for TANGO
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
w = [0.,0.,0.]
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

#--------------------------------------------------------------------
#              Animation controls
#--------------------------------------------------------------------
#Window size to show the data (days)
size_time = 0.5
#1./(photograms per day) in this case the code will create a photogram each 7.2 min
vel_time  = 1./200.
#Animation minimum time (Be sure that you are using the same units as in your data file)
tmin =  2963.2
#Animation maximum time (Be sure that you are using the same units as in your data file)
tmax =  2964.4
#frame rate
frate = 1./50.

#--------------------------------------------------------------------
#                     Plot controls
#--------------------------------------------------------------------

#Labels to appear in the animations
#X-axis of the model plot (upper plot)
xlabel = 'Time [days]'
#Y-axis of the model plot (upper plot)
ylabel = 'Stellar light [%]'
#X and Y-axes for the planets animation
skylabel = 'Sky [$R_\star$]'

#Control colors
#For nice colors in hexagesimal format  see https://www.colorhexa.com/
cmodel = "#34495e"
cdata = "#e74c3c"
cstar = "#ffbf00"

#Control if we want to plot the error bars in the data
is_plot_errorbars = True

#Control if we overplot the light curve model
#You need to have installed pyaneti in your computer to use it
is_plot_model = False

#-----------------------------------------------------------------
#                   Default functions
#-----------------------------------------------------------------

#This function calcualtes the time of periastron given
#Time of minimum conjunction, eccentricit, angle of periastron, period.
def find_tp(T0,e,w,P):
  ereal = e + np.cos(np.pi/2. - w)
  eimag = np.sqrt(1. - e*e) * np.sin( np.pi / 2. - w )
  theta_p = np.arctan2(eimag,ereal)
  theta_p = theta_p - e * np.sin(theta_p)
  Tp = T0 - theta_p * P / 2. / np.pi
  return Tp

#This function calculates the true anomaly
def find_anomaly(t,Tp,e,P):
  mean = 2.*np.pi * ( t - Tp) / P                     #mean anomaly
  true = mean + e * np.sin(mean)                      #guess
  f = true - e * np.sin(true) - mean                  #first value of function f
  for o in range(0,len(t)):                           #iterate for all the values
      while np.abs(f[o]) > 1e-6:                      #Newton-Raphson condition
        f[o] = true[o] - e*np.sin(true[o]) - mean[o]  #calculate  f
        df   = 1. - e * np.cos(true[o])               #Calculate df
        true[o] = true[o] - f[o]/df                   #Update the eccentric anomaly
  eimag = np.sqrt(1. - e*e)*np.sin(true)              #Time to calculate true anomaly
  ereal = np.cos(true) - e
  true  = np.arctan2(eimag,ereal)                     #Get True anomaly from ecc anomaly
  return true

#-----------------------------------------------------------------
#                         END
#-----------------------------------------------------------------