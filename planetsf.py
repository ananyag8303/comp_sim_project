import math
import numpy as np
from numpy.linalg import norm

'''
Planet class helps make this a n body code because new planets can be added without having to alter the main code
'''


class Planet(object):
    
    def __init__(self, name, mass, orbit, colour):
        '''This initializes the class and sets the following attributes for each planet: 
            name, mass, orbital radius, planet colour for the simulation, 
            starting time at 0 for all planets, gravitational constant 
            and a list to store the radial vector values'''
        self.name = name
        # mass in kg
        self.m = mass
        # orbital radius in m
        self.orbit = orbit
        # colour - need to strip trailing line return!
        self.c = colour
        # set year to zero
        self.year = 0
        self.G = 1.18638e-4
        self.vector = []
        
    def initialise(self, G, p):
        '''It begins with setting the initial position of planets with the x coordinate being their 
        orbital radius and the y axis coordinate being 0 so they all start from the y axis at the 
        same point in time. Next it sets the position of the Sun to (0,0) so it stays at the center 
        throughout the simulation. In the same loop, I also linked the velocity values for the satellite 
        being launched and the other planets needed for the simulation. Another loop in the same method 
        helps update the acceleration of the planets while keeping the Sun constant through the simulation duration.'''
        # inital position, initial coords = (orbit radius, 0)
        self.r = np.array([self.orbit, 0])
        # inital velocity, tangential to position
        # speed = sqrt(G*marsmass/r)
        if (self.orbit == 0.0):
            self.v = np.array([0, 0])
        else:
            if self.name == 'Satellite':
                #vel = math.sqrt(self.G*p.m/self.orbit)
                self.v = np.array([3.4,5.4])
            else:
                vel = math.sqrt(self.G*p.m/self.orbit)
                self.v = np.array([0, vel])
                
        # intial accelatation, using gravitational force law
        if (self.orbit == 0.0):
            self.a = np.array([0, 0])
        else:
            self.a = self.updateAcc(G, p)
        # set acc_old = acc to start Beeman
        self.a_old = self.a

    def updatePos(self, G, dt):
        '''This updates the position of the planet according to the Beeman algorithm. 
        It also make sures to keep the old position vector so as to update the year each time it 
        crosses the x axis.'''
        # keep old position to check for year
        self.r_old = self.r
        
        # update position first: Beeman
        self.r = self.r + self.v*dt + (4*self.a - self.a_old)*dt*dt/6.0
        self.vector.append(self.r)
        #print(self.vector)

    def updateVel(self, G, dt, p):
        '''Like the method above, this method updates the velocity according to the Beeman algorithm. 
        It then updates the acceleration of the celestial body for each iteration.'''
        # update velocity second: Beeman
        a_new = self.updateAcc(G, p)
        self.v = self.v + + (2*a_new + 5*self.a - self.a_old)*dt/6.0
        #print(self.v)
        # now update acc ready for next iteration
        self.a_old = self.a
        self.a = a_new
        
        
    def updateAcc(self, G, p):
        '''This updates the acceleration of the object according to the gravitation law.'''
        pos = self.r - p.r
        a = -G*p.m*pos/math.pow(norm(pos),3)
        return a

    def newYear(self):
        '''The loop updates the time taken to complete one orbit around the Sun. 
        This is done by using a loop to update the year as in when the y axis coordinate of the position vector 
        is greater than or equal to zero. To sum up it updates the year as in when it crosses the 
        positive side of the x axis ie (orbital radius,0) coordinate'''
        # update the year when the planet passes the +x axis
        if (self.r_old[1] < 0.0 and self.r[1] >= 0.0):
            self.year +=1
            return True
        else:
            return False

    def kineticEnergy(self):
        '''This calculates the kinetic energy of the planet in joules'''
        ke = (np.dot(self.v, self.v))*self.m/2
        return ke
