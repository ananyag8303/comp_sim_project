#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:08:51 2023

@author: antara
"""

''' THIS FILE IS FOR EXPERIMENT 3 IE SEEING CLOSEST DISTANCE TO MARS'''
import matplotlib.pyplot as plt

class diffplot(object):
    
    
    def __init__(self):
        '''initialises the class and creates the x and y axis lists. '''
        self.float_time = []
        self.float_diff = []
        
    def read_file(self):
        '''reads the external file and stores the formatted values in the above created lists'''
        filename = "diff_data.csv"
        file = open(filename)
        time = []
        diff = []
        x = file.readlines()
        for line in x:
            line = line.rstrip().split()
            time.append(line[0])
            diff.append(line[1])
            
        self.float_diff = [float(i) for i in diff]
        #self.formatted_diff = ["%.4g" % elem for elem in float_diff]
        self.float_time = [float(i) for i in time]
        mini = min(self.float_diff)
        print(f"The minimum distance from Mars is {mini:.3f}")
        index = self.float_diff.index(mini)
        #print(index)
        print(f"The time that this happens is { self.float_time[index] * 365:.3f} months after launch")
        
    def plot_graph(self):
        '''method that plots the graph with respective labels'''
        #plt.plot(self.float_time, self.float_energy)
        plt.plot(self.float_time, self.float_diff)
        plt.title("Time vs Distance from Mars")
        plt.xlabel("Time (earth years)")
        plt.ylabel("Difference in Distance (AU)")
        plt.show()

        
def main():
    d = diffplot()
    d.read_file()
    d.plot_graph()
main()