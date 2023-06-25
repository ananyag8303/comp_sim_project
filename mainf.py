#Importing the planet class from the Planet file created in the same directory
from planetsf import Planet

#Importing the necessary libraries that will be used later
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy.linalg import norm

'''
Class to run the orbital simulation. NOTE THIS FILE CREATES THE MAIN SIMULATION
'''

#Class to run the entire Solar System
class Solar(object):

    def __init__(self):
        #open the parameter file that has all the values, read it and append the values to a list to be used later
        parameters = []
        filename = "parameters.py"
        simulation = open(filename)
        #reading from the 3rd line onwards as the above lines are redundant for this project
        y = simulation.readlines()[3:]
        for line in y:
            #rstrip() to remove trailing characters
            line = line.rstrip()
            #print("line = ", line)
            #To skip over lines that are comments in the file do the following:
            if line[0] != '#':
                parameters.append(line)
        #print(parameters)
        simulation.close()
        #create a file that saves the total energy values 
        self.energy_file = open("beeman_energy_data.csv","w")
        #create a file that saves the distance to Mars values 
        self.diff_file = open("diff_data.csv","w")
        #simulation parameters: number of iterations, delta time and gravitational constant respectively
        self.niter = int(parameters[0])
        self.dt = float(parameters[1])
        self.G = float(parameters[2])
        self.difference = []

        # list for all planets to be stored in 
        self.bodies = []
        
        #appending the respective values for each planets dimension to the list created above
        for i in range(3, len(parameters), 4):
            name = parameters[i]
            mass = float(parameters[i+1])
            orbit = float(parameters[i+2])
            colour = parameters[i+3]
            self.bodies.append(Planet(name, mass, orbit, colour))
                                
        # set initial positions and velocities relative to sun
        # sun must be first element in bodies list
        for i in range(0, len(self.bodies)):
            self.bodies[i].initialise(self.G, self.bodies[0])

    def init(self):
        # initialiser for animator
        return self.patches

    def animate(self, i):
        # keep track of time in earth years
        time = (i+1)*self.dt
        #literature values of orbital periods
        periods = [0.241,0.616,1,1.05,1.88,11.871]
        # update positions
        for j in range(0, len(self.bodies)):
            self.bodies[j].updatePos(self.G, self.dt)
            self.patches[j].center = self.bodies[j].r
            
        # then update velocities
        for j in range(0, len(self.bodies)):
            for k in range(0, len(self.bodies)):
                if (j != k):
                    self.bodies[j].updateVel(self.G, self.dt, self.bodies[k])

        # check year and print year if new year for any planet. Also update total energy at the end of each Earth year
        for j in range(0, len(self.bodies)):
            if (self.bodies[j].newYear()):
               #print(periods[j-1], self.bodies[j].name, j)
               print(self.bodies[j].name.strip() + " calculated period " + str('{:.4}'.format(time/self.bodies[j].year)) + " earth years vs actual period " + str(periods[j-1]))
               if (self.bodies[j].name.strip() == 'Earth'):
                   # need to convert from earth masses AU^2 yr^-2 to kg m^2 s-2 (J)
                   # 1 earth mass = 5.97219e24 kg
                   # 1 AU = 1.496e+11 m
                   c =(5.97219e+24*1.496e+11*1.496e+11)/(3.154e+7*3.154e+7)
                   energy = self.energy()*c
                   print('Time = ' + str('{:3}'.format(time)) + ' earth years. Total energy = ' + '{:.3e}'.format(energy) + ' J')      
                   #write values to the external file created above
                   self.energy_file.write(str(time)+ " " + str(energy)+ "\n")
        # calulate the magnitude of distance between Satellite and Mars. Store these values in external file opened above           
        for j in range(0, len(self.bodies)):
            for k in range(0, len(self.bodies)):
                if self.bodies[j].name.strip() == 'Satellite' and self.bodies[k].name.strip() == 'Mars':
                    difference = math.sqrt((self.bodies[k].vector[i][0]-self.bodies[j].vector[i][0])**2+(self.bodies[k].vector[i][1]-self.bodies[j].vector[i][1])**2)
                    self.diff_file.write(str(time)+ " " + str(difference)+ "\n")
          
        return self.patches
    

    def energy(self):
        ke = 0.0
        pe = 0.0
        for j in range(0, len(self.bodies)):
            ke += self.bodies[j].kineticEnergy()
            for k in range(0, len(self.bodies)):
                if (k != j):
                    r = norm(self.bodies[k].r - self.bodies[j].r)
                    pe -= self.G*self.bodies[j].m*self.bodies[k].m / r
        # divide pe by two to avoid double counting
        pe = pe / 2
        totEnergy = ke + pe
        
        return totEnergy
         
    def closefile1(self):
        #close energy file once simulation is complete
        self.energy_file.close()
        return self.energy_file
    
    def closefile2(self):
        #close the difference file once simulation is shut down
       self.diff_file.close()
       return self.diff_file
    
    def run(self):
        
        # set up the plot components        
        fig = plt.figure()
        ax = plt.axes()
        #ax.set_facecolor("black")
        

        # create an array for patches (planet and moons)
        self.patches = []

        # get orbital radius of outermost planet to set size of orbiting bodies and of plot
        
        maxOrb = math.sqrt(np.dot(self.bodies[-1].r, self.bodies[-1].r))

        # add the planet and moons to the Axes and patches
        for i in range(0, len(self.bodies)):
            if (i == 0):
                self.patches.append(ax.add_patch(plt.Circle(self.bodies[i].r, 0.05*maxOrb, color = self.bodies[i].c, animated = True)))
            else:
                self.patches.append(ax.add_patch(plt.Circle(self.bodies[i].r, 0.02*maxOrb, color = self.bodies[i].c, animated = True)))
        
        # set up the axes
        # scale axes so circle looks like a circle and set limits with border b for prettier plot
        b = 1.05
        lim = maxOrb*b
        img = plt.imread("background.jpeg")
        ax.imshow(img,extent=[-lim,lim,-lim,lim])
        ax.axis('scaled')
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_xlabel('orbital radius(AU)')
        ax.set_ylabel('orbital radius(AU)')   
        plt.title('Simulation of the Solar System')
        
        anim = FuncAnimation(fig, self.animate, init_func = self.init, frames = self.niter, repeat = False, interval = 1, blit= True)
        
        plt.show(block=True)

def main():

    s = Solar()
    s.run()
    s.closefile1()
    s.closefile2()
    
    
main()
