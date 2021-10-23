#---------------------------------------------------------------
#                        TANGO 
#               Animate exoplanet transits!
#              October 2018, Oscar Barragan
#           Updated March 2021, Oscar Barragan
#---------------------------------------------------------------

#Load libraries
from __future__ import print_function, division, absolute_import
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

#number of planets
npl = len(P)

#Read the data file
tvec, fvec, evec = np.loadtxt(system+'/'+lcname,unpack=True,usecols=(0,1,2))

error_mean = np.mean(evec)
sigma3 = 3*error_mean

fvec = fvec*100.
evec = evec*100.

#Estimate number of iterations
niter = int((tmax - tmin)/vel_time)

#Create the flux vector
Tp = [None]*npl
for o in range(npl):
  #Calculate time of periastron
  Tp[o] = find_tp(T0[o],e[o],w[o],P[o])


if is_plot_model:
    from pytransit import QuadraticModel
    #Let us use PyTransit to compute the transits
    xtr_model = np.arange(min(tvec)-size_time,max(tvec)+size_time,0.0001)
    fluxtr_model = [1]*len(xtr_model)
    for o in range(npl):
        tm = QuadraticModel(interpolate=False)
        tm.set_data(xtr_model,exptimes=t_cad,nsamples=n_cad)
        fluxtr_planet = tm.evaluate(k=rp[o], ldc=[u1,u2], t0=T0[o], p=P[o], a=a[o], i=inclination[o])
        #Avoid errors because of occultations calculated by pytransit
        phase = abs(((xtr_model-T0[o])%P[o])/P[o])
        phase[phase>0.5] -= 1
        fluxtr_planet[abs(phase)>0.125] = 1.
        fluxtr_model *= fluxtr_planet
    #Change the model to percentage
    fluxtr_model *= 100

#Let us create the coordinates for the plot
nu = [None]*npl
R = [None]*npl
X = [None]*npl
Y = [None]*npl
min_t =  tmin + size_time/2.0 
ptime = np.arange(min_t,tmax+size_time,vel_time)
for o in range(0,npl):
  nu[o] = find_anomaly(ptime,Tp[o],e[o],P[o])
#We have the true anomaly, time to calculate R
  R[o] = a[o]*(1-e[o]**2)/(1. + e[o]*np.cos(nu[o]) ) 
  X[o] = - R[o] * ( np.cos(nu[o] + w[o]) )
  Y[o] = - R[o] * ( np.sin(nu[o] + w[o]) * np.cos(inclination[o]) )

#Let us find the stellar colour
teff = np.loadtxt('src/colours.dat',unpack=True,comments='!',usecols=0)
col  = np.loadtxt('src/colours.dat',unpack=True,comments='!',usecols=1,dtype=str)
#Let us compute the closses teff to our T_star
difs = abs(teff-T_star)
#Let us select the index that matches better our T_star
cstar = col[np.argmin(difs)]

if cdata == None: cdata = cstar

continuar = True
min_loc = tmin
max_loc = tmin + size_time
n = 1
print('Creating png files')
while continuar:
  estet = []
  estef = []
  estee = []
  modt = []
  modf = []
  for o in range(len(tvec)):
    if ( tvec[o] > min_loc and tvec[o] < max_loc ):
      estet.append(tvec[o])
      estef.append(fvec[o])
      estee.append(evec[o])

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
  if dark_mode: plt.style.use('dark_background')
  fsize = 6
  df = 0.13*(100.-min(fvec))
  fig = plt.figure(1,figsize=(fsize,fsize))
  #plt.xkcd()
  gs = gridspec.GridSpec(nrows=2, ncols=1,height_ratios=[1.4, 1.])
  ax0 = plt.subplot(gs[0])
  plt.ylim(min(fvec)-df,max(fvec)+df)
  plt.xlim(min_loc,min_loc+size_time)
  plt.axvline(x=min_loc+size_time/2.,c='r',ls='--')
  plt.ticklabel_format(useOffset=False, axis='y')
  plt.ticklabel_format(useOffset=False, axis='x')
  if is_plot_errorbars :
    plt.errorbar(estet,estef,estee,fmt='o',color=cdata)
  else:
    plt.plot(estet,estef,'o',color=cdata,alpha=0.5)
  if is_plot_model: plt.plot(modt,modf,'k',color=cmodel,zorder=5)
  plt.minorticks_on()
  plt.tick_params( axis='x',which='both',direction='in')
  plt.tick_params( axis='y',which='both',direction='in')
  plt.tick_params(labelsize=fsize)
  plt.xlabel(xlabel,fontsize=fsize)
  plt.ylabel(ylabel,fontsize=fsize)
  xticks = ax0.get_xticks()
  xticks = list(xticks)
  for j in range(0,len(xticks)):
      xticks[j] = round(xticks[j],3)
  #ax0.set_xticklabels(xticks)
  ax0.set_xticklabels(xticks[0:len(xticks)-2])
#---------------------------------------------------------------
#                         Star-planets
#---------------------------------------------------------------
  ax1 = plt.subplot(gs[1])
  star = plt.Circle((0,0),1.0,color=cstar)
  ax1.add_artist(star)
  planet = [None]*npl
  for j in range(0,npl):
    #if ( Y[j][n-1] < 0 or np.sqrt(X[j][n-1]**2 + Y[j][n-1]**2) > 1 ):
    if ( Y[j][n-1] < 0 or np.sqrt(X[j][n-1]**2 + Y[j][n-1]**2) > 1 ):
      pcolor = 'k'
      if dark_mode: pcolor = '#ffffff'
      planet[j] = plt.Circle((X[j][n-1],Y[j][n-1]),rp[j],color=pcolor)
      ax1.add_artist(planet[j])
  plt.xlim(-4,4)
  if xaxis_log:
    plt.xlim(-xlimit,xlimit)
    plt.xscale('symlog')
  plt.minorticks_on()
  plt.ylim(-1.5,1.5)
  plt.tick_params( axis='x',which='both',direction='in')
  plt.tick_params( axis='y',which='both',direction='in')
  plt.xlabel(skylabel,fontsize=fsize)
  plt.ylabel(skylabel,fontsize=fsize)
  plt.tick_params(labelsize=fsize)
  plt.annotate(system,xy=(0.12,0.37),xycoords='figure fraction',alpha=0.5,fontsize=10)
#
  file_name = system + '/' + system + '-'
  m = n
  if (n == 0):
    m = 1
  for j in range(0,int(np.log10(niter))-int(np.log10(m))):
     file_name = file_name + '0'
  file_name = file_name+str(n)+'.png'
  fig.set_size_inches(fsize,fsize)
  #plt.savefig(file_name,dpi=300,bbox_inches='tight')
  #plt.style.use('dark_background')
  #plt.savefig(file_name,bbox_inches='tight',transparent=True)
  plt.savefig(file_name,bbox_inches='tight')
  plt.close()
  #Now let us evolve the video
  min_loc = min_loc + vel_time
  max_loc = max_loc + vel_time
  if ( max_loc > tmax ):
    continuar = False
  else:
    n = n + 1

print('png files have been created')
#---------------------------------------------------------------
#                      END plot creation
#---------------------------------------------------------------
#                    Start  movie creation
#---------------------------------------------------------------

exec(open('src/moviepy_src.py').read())

#---------------------------------------------------------------
#                    End movie creation
#---------------------------------------------------------------
