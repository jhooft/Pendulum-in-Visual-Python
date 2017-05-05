#modify simple pendulum system to incorporate free horizontal slider:
#note to self: will Decimal() fix the overflow issue??

from scipy.integrate import odeint
from matplotlib import pylab as plt
import numpy as np

##############initial conditions###################
theta0= 1*np.pi/5 #initial angle in radians        theta=0 is straight up
thetadot0 = 0. #initial angular velocity of pend
atheta0 = 0.0 #initial angular accel
p0 = 0. #initial slider position
pdot0 = 0. # initial slider velocity
ap0 = 0. #initial slider acceleration
###################################################

#################Constants#########################
m=1 #mass of pendulum (kg)
alpha = 10. #ratio of pivot mass to pendulum mass
g=9.8 #gravitational accel (m/s^2)
r=1 #length of pendulum arm (m)
###################################################

theta = theta0 #theta is measured from 0 radians when pend is straight up and is positive to the left
thetadot = thetadot0
atheta= atheta0
dtheta0 = 0.
dtheta = dtheta0
p=p0
pdot=pdot0
ap=ap0

def rhs(q, t):
    theta, thetadot, p, pdot = q
    theta = theta%(2*np.pi)
     
    atheta = ((1+alpha*m)/(1+alpha*m-np.cos(theta)**2))*(g*np.sin(theta)/r-thetadot**2*np.sin(theta)*np.cos(theta)/(1+alpha*m))
    ap = (r*thetadot**2*np.sin(theta)-g*np.sin(theta)*np.cos(theta))/(1+alpha*m-np.cos(theta)**2)
    return [thetadot, atheta, pdot, ap]

T=10.
steps= 500.   #correspond to dt=.02??
q0 = ([theta0, thetadot0,p0, pdot0])
ts = np.linspace(0, T, steps)
q1,q2,p1,p2 = odeint(rhs, q0, ts).T

plt.plot(ts, q1, color = 'pink')
plt.plot(ts, q2, color = 'yellow')
plt.plot(ts, p1, color = 'purple')

T=10.
steps= 500.   
ts = np.linspace(0, T, steps)
plt.xlabel('t')
plt.title('FREE HORIZONTAL SLIDING PIVOT\nAngle theta (from vertical) is red - ODEINT pink\n Angular velocity is green - ODEINT yellow\n Pivot position is blue - ODEINT purple')
plt.ylabel('mass ratio: '+str(alpha))
dt=.02
#i=0
count = 0
Q1 = np.arange(0,500, dtype = float)    #Q1 will hold the vector of angles
Q2=np.arange(0,500,dtype=float)         #Q2 will hold the vector of angular accelerations
P1=np.arange(0,500,dtype=float)         #P1 will hold the vector of pivot positions
#P2=np.arange(0,500,dtype=float)
Q1[0]=theta0 
Q2[0]=thetadot0 
P1[0]=p0
#P2[0]=pdot0

while count < 500:
    count+=1   
    
    #atheta = (g/r)*np.sin(theta)-(ap/r)*np.cos(theta)
    #ap = (r*thetadot**2*np.sin(theta)-r*atheta*np.cos(theta))/(1+alpha*m) 
    atheta = ((1+alpha*m)/(1+alpha*m-np.cos(theta)**2))*(g*np.sin(theta)/r-thetadot**2*np.sin(theta)*np.cos(theta)/(1+alpha*m))
    ap = (r*thetadot**2*np.sin(theta)-g*np.sin(theta)*np.cos(theta))/(1+alpha*m-np.cos(theta)**2)
    
    thetadot += atheta*dt
    theta += thetadot*dt
    pdot += ap*dt
    p += pdot*dt
    
    if count < 500:
        Q1[count] = theta
        Q2[count] = thetadot
        P1[count] = p
    #if count%20==0:
        #print ('theta: ',theta,' vel: ',thetadot,' pos ',p,' ap ', ap)
plt.plot(ts, Q1, color = 'red')
plt.plot(ts, Q2, color = 'green')
plt.plot(ts, P1, color = 'blue')