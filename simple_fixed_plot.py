#math only for simplest pendulum case with fixed pivot

from scipy.integrate import odeint
from matplotlib import pylab as plt
import numpy as np

##############initial conditions###################
theta0 = .2 #initial angle in radians, theta=0 is straight up
thetadot0 = 0.3  #initial angular velocity of pend
atheta0 = 0.0 #initial angular accel
###################################################

#################Constants#########################
m = 1 #mass of pendulum (kg)
g = 9.8 #gravitational accel (m/s^2)
r = 1 #length of pendulum arm (m)
###################################################

theta = theta0 
thetadot = thetadot0
atheta = atheta0

def rhs(q, t):
    theta, thetadot = q
    
    if theta < 0:        ##keep theta between 0 and 2pi
        theta += 2*np.pi ##
    if theta > 2*np.pi:  ##
        theta -= 2*np.pi ##
    atheta = (g/r)*np.sin(theta)    #equation of motion for simple pendulum
        
    return [thetadot, atheta]

T=10.
steps= 500.   #correspond to dt=.02??
q0 = ([theta0, thetadot0])
ts = np.linspace(0, T, steps)
q1,q2 = odeint(rhs, q0, ts).T


plt.plot(ts, q1, color='r')
#print(len(ts))
plt.xlabel('t')
plt.ylabel('Initial theta: '+str(theta0)+'\nInitial vel: '+str(thetadot0))
plt.title('Comparison of Methods for Simple Pendulum Case\nODEINT: angle theta (from vertical) is red, angular velocity is green \n MANUAL: angle is pink, velocity is blue')
plt.plot(ts, q2, color='g')
#duration = 30.0
dt=.02
#i=0
count = 0
Q1 = np.arange(0,500, dtype = float)
#print(len(Q1))
Q2=np.arange(0,500,dtype=float)
Q1[0]=theta0#+.2
#print(theta0)
#print(Q1[0])
Q2[0]=thetadot0#+.2
theta = theta0
while count < 500:
    count+=1   
    #if theta <0:         ##keep theta between 0 and 2pi  for purpose of case handling in accelerate_slider()
        #theta += 2*np.pi ##
    #if theta > 2*np.pi:  ##
        #theta -= 2*np.pi ##
    atheta = (g/r)*np.sin(theta)
    thetadot += atheta*dt
    theta += thetadot*dt
    if count < 500:
        Q1[count]= theta#+.2
        
        Q2[count]=thetadot#+.2
    
plt.plot(ts, Q1, color='pink')

plt.plot(ts, Q2, color='blue')