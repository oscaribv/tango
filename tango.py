import sys
from matplotlib import gridspec
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyaneti as pti
sns.set_color_codes()
sns.set(style='ticks')

lang = 'english' #english or spanish

fname = 'GJ9827_new_lc.dat'

size_time = 0.5 #days
vel_time  = 1./100.
tmax =  2. #days
tmin =  7796 - 7738.4

#colors
cmodel = "#34495e"
cdata = "#e74c3c"
cstar = "#ffbf00"

is_plot_errorbars = True

#Create the system model
P =[1.2089662,3.6482269,6.2014190]
T0 = [7738.8264631,7738.5496113,7740.9619764]
e = [0,0,0]
w = [0,0,0]
rp = [0.0232259,0.0181983,0.0299279]
inclination = [88.330714*np.pi/180,89.06*np.pi/180,87.702*np.pi/180]
a = [7.229235,15.096,21.5019118]
u1 =  0.5771
u2 =   0.146
n_cad = 10
t_cad = 30./60./24.

#number of planets
npl = len(P)

#Read the data file
t, f, e = np.loadtxt(fname,unpack=True,usecols=(0,1,2))

tmax =  min(t) + tmin + tmax

error_mean = np.mean(e)
sigma3 = 3*error_mean

f = f*100.
e = e*100.

#Create the flux vector
pars2 = np.zeros(shape=(npl,7))
for o in range(0,npl):
  #Calculate time of periastron
  Tp = pti.find_tp(T0[o],e[o],w[o],P[o])
  #Fill vector with parameters
  pars2[o][:] = [Tp,P[o],e[o],w[o],inclination[o],a[o],rp[o]]

xtr_model = np.arange(min(t),max(t),0.001)
fluxtr_model = pti.flux_tr(xtr_model,pars2.transpose(),[0,0,0,0],[u1,u2],n_cad,t_cad)
fluxtr_model = fluxtr_model*100

#Let us create the coordinates for the plot
nu = [None]*npl
R = [None]*npl
X = [None]*npl
Y = [None]*npl
min_t = min(t) + tmin + size_time/2.0 
ptime = np.arange(min_t,max(t),vel_time)
for o in range(0,npl):
  nu[o] = pti.find_anomaly_tp(ptime,pars2[o][0],e[o],P[o]) 
#We have the true anomaly, time to calculate R
  R[o] = a[o]*(1-e[o]**2)/(1. + e[o]*np.cos(nu[o]) ) 
  X[o] = - R[o] * ( np.cos(nu[o] + w[o]) )
  Y[o] = - R[o] * ( np.sin(nu[o] + w[o]) * np.cos(inclination[o]) )
#


continuar = True
min_loc = min(t) + tmin
max_loc = min(t) + tmin + size_time
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
  plt.plot(modt,modf,'k',color=cmodel)
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
  file_name = 'system-'
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
