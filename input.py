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

