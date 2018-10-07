#---------------------------------------------------------------
#       TANGO: Transit ANimation for General Orbits 
#             October 2018, Oscar Barragan
#---------------------------------------------------------------

#Readme file

#Load libraries
import sys
import os
from matplotlib import gridspec
import numpy as np
import matplotlib.pyplot as plt

#Start TANGO as ./tango.py system
system = str(sys.argv[1])

execfile(system+'/input.py')

#number of planets
npl = len(P)

#Read the data file
t, f, e = np.loadtxt(system+'/'+lcname,unpack=True,usecols=(0,1,2))

error_mean = np.mean(e)
sigma3 = 3*error_mean

f = f*100.
e = e*100.

#This function calcualtes the time of periastron given
#Time of minimum conjunction, eccentricit, angle of periastron, period.
#----------------------------------------------------------
def find_tp(T0,e,w,P):
  ereal = e + np.cos(np.pi/2. - w)
  eimag = np.sqrt(1. - e*e) * np.sin( np.pi / 2. - w )
  theta_p = np.arctan2(eimag,ereal)
  theta_p = theta_p - e * np.sin(theta_p)
  Tp = T0 - theta_p * P / 2. / np.pi
  return Tp

#This function calculates the true anomaly
#----------------------------------------------------------
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
#----------------------------------------------------------

#Create the flux vector
pars2 = np.zeros(shape=(npl,7))
for o in range(0,npl):
  #Calculate time of periastron
  #Tp = pti.find_tp(T0[o],e[o],w[o],P[o])
  Tp = find_tp(T0[o],e[o],w[o],P[o])
  #Fill vector with parameters
  pars2[o][:] = [Tp,P[o],e[o],w[o],inclination[o],a[o],rp[o]]


if is_plot_model:
  #Import pyaneti code
  import pyaneti as pti
  xtr_model = np.arange(min(t),max(t),0.0025)
  fluxtr_model = pti.flux_tr(xtr_model,pars2.transpose(),[0,0,0,0],[u1,u2],n_cad,t_cad)
  fluxtr_model = fluxtr_model*100

#Let us create the coordinates for the plot
nu = [None]*npl
R = [None]*npl
X = [None]*npl
Y = [None]*npl
min_t =  tmin + size_time/2.0 
ptime = np.arange(min_t,max(t),vel_time)
for o in range(0,npl):
  nu[o] = find_anomaly(ptime,pars2[o][0],e[o],P[o])
#We have the true anomaly, time to calculate R
  R[o] = a[o]*(1-e[o]**2)/(1. + e[o]*np.cos(nu[o]) ) 
  X[o] = - R[o] * ( np.cos(nu[o] + w[o]) )
  Y[o] = - R[o] * ( np.sin(nu[o] + w[o]) * np.cos(inclination[o]) )
#


continuar = True
min_loc = tmin
max_loc = tmin + size_time
n = 1
while continuar:
  estet = []
  estef = []
  estee = []
  modt = []
  modf = []
  for o in range(len(t)):
    if ( t[o] > min_loc and t[o] < max_loc ):
      estet.append(t[o]) 
      estef.append(f[o]) 
      estee.append(e[o]) 

  #model
  if is_plot_model:
    for o in range(len(xtr_model)):
      if ( xtr_model[o] > min_loc and xtr_model[o] < max_loc - size_time/2. ):
        modt.append(xtr_model[o])
        modf.append(fluxtr_model[o])
  #At this point we have all the data inside the window
  #time to plot
#---------------------------------------------------------------
#                         DATA
#---------------------------------------------------------------
  df = 0.13*(100.-min(f))
  plt.figure(1,figsize=(8.,8.))
  #plt.xkcd()
  gs = gridspec.GridSpec(nrows=2, ncols=1,height_ratios=[1.4, 1.])
  plt.subplot(gs[0])
  plt.ylim(min(f)-df,max(f)+df)
  plt.xlim(min_loc,min_loc+size_time)
  plt.axvline(x=min_loc+size_time/2.,c='r',ls='--')
  plt.ticklabel_format(useOffset=False, axis='y')
  plt.ticklabel_format(useOffset=False, axis='x')
  if is_plot_errorbars :
    plt.errorbar(estet,estef,estee,fmt='o',color=cdata)
  else:
    plt.plot(estet,estef,'o',color=cdata)
  if is_plot_model: plt.plot(modt,modf,'k',color=cmodel)
  plt.minorticks_on()
  plt.tick_params( axis='x',which='both',direction='in')
  plt.tick_params( axis='y',which='both',direction='in')
  if lang == 'spanish' : 
    plt.xlabel('Tiempo en dias')
    plt.ylabel('Porcentaje de luz de la estrella')
  if lang == 'english' : 
    plt.xlabel('Time [days]')
    plt.ylabel('Stellar ligth [%]')
#---------------------------------------------------------------
#                         Star-planets
#---------------------------------------------------------------
  ax1 = plt.subplot(gs[1])
  star = plt.Circle((0,0),1.0,color=cstar)
  ax1.add_artist(star)
  planet = [None]*npl
  for j in range(0,npl):
    if ( Y[j][n-1] < 0 or np.sqrt(X[j][n-1]**2 + Y[j][n-1]**2) > 1 ):
      planet[j] = plt.Circle((X[j][n-1],Y[j][n-1]),rp[j],color='k')
      ax1.add_artist(planet[j])
  plt.xlim(-4,4)
  plt.ylim(-1.5,1.5)
  plt.tick_params( axis='x',which='both',direction='in')
  plt.tick_params( axis='y',which='both',direction='in')
  if lang == 'spanish' : 
    plt.xlabel('Cielo')
    plt.ylabel('Cielo')
  if lang == 'english' : 
    plt.xlabel('Sky [$R_\star$]')
    plt.ylabel('Sky [$R_\star$]')
  plt.annotate('@oscaribv',xy=(0.84,0.91),xycoords='figure fraction',alpha=0.7,fontsize=10)
#
  file_name = system + '/' + system + '-'
  m = n
  if (n == 0):
    m = 1
  for j in range(0,int(np.log10(len(t)))-int(np.log10(m))):
     file_name = file_name + '0'
  file_name = file_name+str(n)+'.png'
  plt.savefig(file_name,dpi=150,bbox_inches='tight')
  plt.close()
  #Now let us evolve the video
  min_loc = min_loc + vel_time
  max_loc = max_loc + vel_time
  if ( max_loc > tmax ):
    continuar = False
  else:
    n = n + 1
#---------------------------------------------------------------
#                      END plot creation
#---------------------------------------------------------------
#                    Start  movie creation
#---------------------------------------------------------------

os.system('convert -delay 1/20 -resize x700  '+system+'/*.png '+system+'/'+system+'.mp4')

#---------------------------------------------------------------
#                    End movie creation
#---------------------------------------------------------------