
import matplotlib.pyplot as plt

class energyplot(object):
    
    
    def __init__(self):
        '''initialises the class and creates the x and y axis lists. '''
        self.float_time = []
        self.float_energy = []
        self.formatted_energy = []
    def read_file(self):
        '''reads the external file and stores the formatted values in the above created lists'''
        time = []
        energy = []
        filename = "beeman_energy_data.csv"
        file = open(filename)
        
        x = file.readlines()
        for line in x:
            line = line.rstrip().split()
            time.append(line[0])
            energy.append(line[1])
            
        self.float_energy = [float(i) for i in energy]
        self.float_time = [float(i) for i in time]
           
        self.formatted_energy = ["%.4g" % elem for elem in self.float_energy]
        #print(self.float_time, self.formatted_energy)
     
    def plot_graph(self):
        '''method that plots the graph with respective labels'''
        #plt.plot(self.float_time, self.float_energy)
        plt.plot(self.float_time, self.formatted_energy)
        plt.title("Time vs Energy")
        plt.xlabel("Time (earth years)")
        plt.ylabel("Energy (J)")
        plt.show()

        
def main():
    e = energyplot()
    e.read_file()
    e.plot_graph()
main()
