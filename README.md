# comp_sim_project
This Python project aims to simulate the Solar System using object oriented programming and has additional experiments added
on top of it. While this code only includes planets till Jupiter,a user can account for the other gas giants by including their 
data to the parameters.py file. Below is a breakdown and summary of how to navigate this directory

parameters.py is the main external file for the main simulation as well as experiments. It is here that all the celestial body data is stored. 

1. MAIN SIMULATION
- planetsf.py is the file where the planet class is introduced and this keeps the project a many body simulation
- mainf.py is the file where the animation runs from and is also where the external files are created for values to be stored in them

2. EXPERIMENT 1 (ORBITAL PERIOD)
 - This is integrated into the mainf.py file where at the completion of every orbit, the code generates the simulated value alongside the literature value

3. EXPERIMENT 2 (TOTAL ENERGY OF SYSTEM)
- In the mainf.py file, there is an external file called ‘beeman_energy_data’ being created where total energy values are stored every earth year. 
- energytrial.py file is where the values from the external file are read and plotted as a graph to see the variation of total energy with time.

4. EXPERIMENT 3 (SATELLITE TO MARS)
- The satellite was added as a body in the parameters file. 
- The velocity for this was set in the planetsf.py file
- Magnitude of distance was calculated in the mainf.py file and stored in an external file called ‘diff_data’ 
- difftrial.py plots the magnitudes (distance) as a function of time to determine minimum distance to Mars and its respective time period.

The sole contributor to this project is Ananya Ganapathy. 
