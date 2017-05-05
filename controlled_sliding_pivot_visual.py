#visualization of the sliding pivot with additional external control

import vpython as vp
from vpython import vec, color
import time
import numpy as np
from math import sin, cos
#from decimal import Decimal

#GlowScript bits
scene = vp.canvas()
scene.width =1000
scene.height = 650
scene.range = 1.8
scene.title = "Moveable Pendulum"
#scene.visible = True
t0=time.time()
duration = 20.0 #seconds to run simulation

##############  initial conditions  ##############
theta0=0.2#initial angle         theta=0 is straight up, theta increases clockwise
thetadot0 = 0.3 #initial angular velocity of pend
atheta0 = 0. #initial angular accel0
p0 = 0. #initial position of slider
pdot0 = 0. #initial velocity of slider
ap0 = 0. #initial accel of slider
dtheta0 = 0.  #an incremental change of angle
###################################################

#################  Constants  #####################
m=1 #mass of pendulum
alpha=5. #ratio of pivot mass to pendulum mass
g=9.8 #gravitational accel
r=1 #length of pendulum arm
###################################################

################  Limitations  ####################
p_min = -1.7   #leftmost slider position      ####are these values compatible between graphics, ODE's??????
p_max = 1.7    #rightmost slider position
ap_max=3. #maximum acceleration of slider         #####i picked this number at random
pdot_max = 5.  #picked at random
###################################################


p = p0 #p is x-coordinate of the slider/pivot
pdot = pdot0
ap=ap0
theta = theta0 #theta is measured from 0 radians when pend is straight up and is positive to the left
thetadot = thetadot0
atheta= atheta0
dtheta = dtheta0
ap_adjust = 0



#####################the build assembly##############################
rod = vp.cylinder( pos=vec(-2.7,-.2,0), axis=vec(5.4,0,0), color = color.green, radius=0.02 )
rodlimitmarkleft = vp.cylinder( pos=vec(-1.7,-.2,0), axis=vec(.1,0,0), color = color.yellow, radius=0.02 )
rodlimitmarkright = vp.cylinder( pos=vec(1.7,-.2,0), axis=vec(.1,0,0), color = color.yellow, radius=0.02 )
supportleft = vp.box( pos=vec(-2.7,-1.3,0), color = color.red, size=vec(.1,2.2,.1) )
supportright = vp.box( pos=vec(2.7,-1.3,0), color = color.red, size=vec(.1,2.2,.1) )
slider = vp.box(pos=vec(p,rod.pos.y,0),color = color.red, size=vec(.1,.1,.1))
axlepin = vp.cylinder( pos=vec(slider.pos.x,slider.pos.y,slider.pos.z+0.1), axis=vec(0,0,.2), color = color.yellow, radius=0.02 )
pendulumarm = vp.cylinder(pos=vec(axlepin.pos.x,axlepin.pos.y,axlepin.pos.z+0.2), axis=vec(float(r)*cos(np.pi/2-float(theta)),float(r)*sin(np.pi/2-float(theta)),0), color = color.green, radius=0.02 )
pendulummass = vp.sphere(radius=.1,pos=vec(axlepin.pos.x+float(r)*cos(np.pi/2-float(theta)),axlepin.pos.y+float(r)*sin(np.pi/2-float(theta)),.3))
#pend = vp.compound([pendulumarm,pendulummass])       #????????
pivot = vec(axlepin.pos.x,axlepin.pos.y,axlepin.pos.z+.2)
######################################################################

#EQUATIONS OF MOTION
#atheta = ((1+alpha*m)/(1+alpha*m-np.cos(theta)**2))*(g*np.sin(theta)/r-thetadot**2*np.sin(theta)*np.cos(theta)/(1+alpha*m))
#ap = (r*thetadot**2*np.sin(theta)-g*np.sin(theta)*np.cos(theta))/(1+alpha*m-np.cos(theta)**2)

wait = False
hit_end = False

hit_right = False
hit_left = False
mark = 0.
dt = .05
#count = 0
time.sleep(3)
while time.time() < (t0 + duration):
    vp.rate(10)
    theta = theta%(2*np.pi)
    if time.time() - mark >= 5.:
        wait = False
        
    ##how to proceed if pivot has room to move    
    if hit_end == False:
        atheta = ((1+alpha*m)/(1+alpha*m-np.cos(theta)**2))*(g*np.sin(theta)/r-thetadot**2*np.sin(theta)*np.cos(theta)/(1+alpha*m))
                 
        #####add in external control statements to try to balance the pivot
        if wait == False:
            if ((theta >0) and (theta <= np.pi/4)):                   #octant 1
                if thetadot>0: #if falling
                    ap_adjust = 20.
                    print ('ap20')
                    wait = True
                    mark = time.time()
                
            elif ((theta >np.pi/4) and (theta <= np.pi/2)):           #octant 2
                if thetadot >0:
                    ap_adjust =40.  
                    print('ap40')
                    wait = True
                    mark = time.time()
                
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
                    ap_adjust = -40.
                    print('ap-40')
                    wait = True
                    mark = time.time()
                
            else: #theta is between 7pi/4 and 2pi                     #octant 8
                if thetadot <0:
                    ap_adjust =-20.
                    print('ap-20')
                    wait = True
                    mark = time.time()
                
        ap = (r*thetadot**2*np.sin(theta)-r*atheta*np.cos(theta))/(1+alpha*m)+ap_adjust
        thetadot += atheta*dt
        theta+=thetadot*dt
        dtheta = thetadot*dt
        pdot += ap*dt
        p+=pdot*dt
        if p>p_max:
            hit_right = True
            hit_end = True
        elif p<p_min:
            hit_left = True
            hit_end = True
        if hit_end ==True:   
            pdot = 0
            ap = 0 
            
    ####how to proceed if the slider is 'stopped' at either end
    
    else: 
        atheta = (g/r)*sin(theta) # +Decimal(.1) #-(ap/r)*Decimal(cos(theta))        for the reset cycle, I forcefully hold ap at zero
        if p<0:         #
            pdot = 4.   # this is slider velocity to 'reset' to center 
        elif p>0:       #
            pdot = -4.  #
        else: #p=0 ie. slider is centered
            hit_end=False
            hit_right=False
            hit_left=False
        thetadot +=  atheta*dt
        theta += thetadot*dt
        dtheta = thetadot*dt
               
        p +=pdot*dt
    
    
    
        thetadot +=  atheta*dt
        theta += thetadot*dt
        dtheta = -thetadot*dt
    
    #update slider position:
    slider.pos.x = p
    #update axlepin position:
    axlepin.pos.x = p
    #update pendarm position/rotation:
    pivot.x=p  
    pendulumarm.pos.x = p
    pendulumarm.rotate(angle = dtheta, axis=vec(0,0,1), origin=pivot)
    pendulummass.pos.x = axlepin.pos.x+float(r)*cos(np.pi/2-float(theta))
    pendulummass.pos.y = axlepin.pos.y+float(r)*sin(np.pi/2-float(theta))
    