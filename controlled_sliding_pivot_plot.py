#incorporating external control over slider acceleration
#cases to be structured so as to try to 'bump' the pendulum back up to its unstable equilibrium position
#this script is for plotting only

from scipy.integrate import odeint
from matplotlib import pylab as plt
import numpy as np

##############initial conditions###################
theta0=np.pi/16 #initial angle in radians        theta=0 is straight up
thetadot0 = 0. #initial angular velocity of pend
atheta0 = 0.0 #initial angular accel
p0 = 0. #initial position of slider
pdot0 = 0. #initial velocity of slider
ap0 = 0.0 #initial accel of slider
###################################################

#################Constants#########################
m=1 #mass of pendulum (kg)
alpha = 2. #ratio of pivot mass to pendulum mass
g=9.8 #gravitational accel (m/s^2)
r=1 #length of pendulum arm (m)
###################################################

p = p0 
pdot = pdot0
ap=ap0
theta = theta0 
thetadot = thetadot0
atheta= atheta0
dtheta0 = 0.
dtheta = dtheta0

#EQUATIONS OF MOTION
#atheta = (g/r)*Decimal(sin(theta))-(ap/r)*Decimal(cos(theta))
#ap = r*thetadot**2*Decimal(sin(theta))-r*atheta*Decimal(cos(theta))

def rhs(q, t):
    theta, thetadot, p, pdot = q
    #dt = .01
    #if (theta<0 or theta > 2*np.pi):
    theta = theta%(2*np.pi)
    ap_adjust = 0.
    #ap = pdot*dt            ##this is my clumsy attempt to simulate the need for simultaneous updating of ap and atheta
    atheta = ((1+alpha*m)/(1+alpha*m-np.cos(theta)**2))*(g*np.sin(theta)/r-thetadot**2*np.sin(theta)*np.cos(theta)/(1+alpha*m))
    
    #atheta = (g/r)*np.sin(theta)-(ap/r)*np.cos(theta)
    if ((theta >0) and (theta <= np.pi/4)):                #octant 1
        if thetadot>0:  #if falling
            
            ap_adjust = 5.
            #print ('ap: ',ap,'ap_adj',ap_adjust)
    elif ((theta >np.pi/4) and (theta <= np.pi/2)):        #octant 2
        if thetadot >0:
            ap_adjust =10.
            #print ('ap: ',ap,'ap_adj',ap_adjust)
    elif ((theta >np.pi/2) and (theta <= 3*np.pi/4)):         #octant 3   
            #if thetadot >=0:
             #   ap_adjust = -2
            #else:
             #   ap_adjust = .2                             
            blank = 0
    elif ((theta >3*np.pi/4) and (theta <= np.pi)):           #octant 4
            #if thetadot >0:
             #   ap_adjust =-.5
            blank = 0
    elif ((theta >np.pi) and (theta <= 5*np.pi/4)):           #octant 5
            #if thetadot <0:
             #   ap_adjust =.5
            blank = 0
    elif ((theta >5*np.pi/4) and (theta <= 3*np.pi/2)):       #octant 6            
            blank = 0  
    elif ((theta > 3*np.pi/2) and (theta <= 7*np.pi/4)):   #octant 7
        if thetadot <0:
            ap_adjust =-10.
            #print ('ap: ',ap,'ap_adj',ap_adjust)
    else: #theta is between 7pi/4 and 2pi
        if thetadot <0:
            ap_adjust =-5.   
            #print('ap: ',ap,'ap_adj',ap_adjust)
    #ap = r*thetadot**2*np.sin(theta)-r*atheta*np.cos(theta) + ap_adjust
    ap = (r*thetadot**2*np.sin(theta)-g*np.sin(theta)*np.cos(theta))/(1+alpha*m-np.cos(theta)**2)+ ap_adjust
    
    return [thetadot, atheta, pdot, ap]
  

T=10.
steps= 500.
q0 = ([theta0, thetadot0, p0, pdot0])
ts = np.linspace(0, T, steps)
q1,q2,q3,q4 = odeint(rhs, q0, ts).T

plt.plot(ts, q1, color='pink',label = 'angle')
plt.plot(ts, q2, color = 'yellow',label = 'vel')
plt.plot(ts, q3, color = 'purple',label = 'pivot')

#print(qs[0],qs[5],qs[10],qs[20])
#print(dqs[0],dqs[5],dqs[10],dqs[20])
plt.xlabel('t')
plt.ylabel('mass ratio: '+str(alpha))
plt.title('EXTERNAL CONTROL ON SLIDING PIVOT\nAngle theta (from vertical) is red,\n Angular velocity is green,\nPivot position is blue')

Q1 = np.arange(0,500, dtype = float)    #Q1 will hold the vector of angles
Q2 = np.arange(0,500,dtype=float)         #Q2 will hold the vector of angular accelerations
P1 = np.arange(0,500,dtype=float)         #P1 will hold the vector of pivot positions
#P2=np.arange(0,500,dtype=float)
Q1[0]=theta0 
Q2[0]=thetadot0 
P1[0]=p0
wait = False      #need to control brief impulse and wait for effect on system, rather than applying sustained force
mark = 0
dt = .02
count = 0
blank = 0
while count < 500:
    count+=1   
    if count - mark >= 5:
        wait = False
    #atheta = (g/r)*np.sin(theta)-(ap/r)*np.cos(theta)
    atheta = ((1+alpha*m)/(1+alpha*m-np.cos(theta)**2))*(g*np.sin(theta)/r-thetadot**2*np.sin(theta)*np.cos(theta)/(1+alpha*m))
    ap_adjust = 0.
       
    if wait == False:
        if ((theta >0) and (theta <= np.pi/4)):                   #octant 1
            if thetadot>0: #if falling
                ap_adjust = 10.                                  
                wait = True
                mark = count
                #print ('count: ',count,' ap1')
        elif ((theta >np.pi/4) and (theta <= np.pi/2)):           #octant 2
            if thetadot >0:
                ap_adjust =20.                                    
                wait = True
                mark = count
                #print('count: ',count,' ap2')
        elif ((theta >np.pi/2) and (theta <= 3*np.pi/4)):         #octant 3   
            #if thetadot >=0:
             #   ap_adjust = -2
            #else:
             #   ap_adjust = .2                             
            blank = 0
        elif ((theta >3*np.pi/4) and (theta <= np.pi)):           #octant 4
            #if thetadot >0:
             #   ap_adjust =-.5
            blank = 0
        elif ((theta >np.pi) and (theta <= 5*np.pi/4)):           #octant 5
            #if thetadot <0:
             #   ap_adjust =.5
            blank = 0
        elif ((theta >5*np.pi/4) and (theta <= 3*np.pi/2)):       #octant 6            
            blank = 0  
                
        elif ((theta > 3*np.pi/2) and (theta <= 7*np.pi/4)):      #octant 7
            if thetadot <0:
                ap_adjust = -20.
                wait = True
                mark = count
                #print('count: ',count,' ap7')
        else: #theta is between 7pi/4 and 2pi                     #octant 8
            if thetadot <0:
                ap_adjust =-10.
                wait = True
                mark = count
                #print('count: ',count,' ap8')
        ap = (r*thetadot**2*np.sin(theta)-r*atheta*np.cos(theta))/(1+alpha*m)+ap_adjust
    #else:
    ap = (r*thetadot**2*np.sin(theta)-r*atheta*np.cos(theta))/(1+alpha*m)
    thetadot += atheta*dt
    theta += thetadot*dt
    pdot += ap*dt
    p += pdot*dt
    
    if count < 500:
        Q1[count] = theta
        Q2[count] = thetadot
        P1[count] = p
    #if count%10==0:
        #print ('theta: ',theta,' vel: ',thetadot,' pos ',p,' ap ', ap)
plt.plot(ts, Q1, color = 'red')
plt.plot(ts, Q2, color = 'green')
plt.plot(ts, P1, color = 'blue')    
    

    #if abs(pdot) < pdot_max:
    #pdot += ap*dt
    #if Decimal(abs(p)) < p_max:  ####the slider is within its boundaries
        #p=Decimal(p)
        #p += pdot*dt
    #else:     ####the slider has hit one of its horizontal boundaries
        #if p > Decimal(0):
            #p = p_max
        #else:
            #p = p_min
        #pdot = Decimal(0)
        #ap = Decimal(0)