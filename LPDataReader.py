# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:31:58 2019

@author: Frank Pintor
"""

__author__ = 'Dania'
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.figure import Figure
import tkinter as tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import random

indexes = []

x_newTime = [] ##Easy way to visualize time
y_samples = []
y_min = []


class mclass:
    def __init__(self,  window):
        # Labels
        self.openFileLabel = tk.Label(window, text="Select file")
        self.openFileLabel.grid(column=1, row=0)
        
        self.samplesLabel = tk.Label(window, text="Number of samples")
        self.samplesLabel.grid(column=50, row=0)
        
        self.plotLabel = tk.Label(window, text="Plot?")
        self.plotLabel.grid(column=60, row=0)
        
        # Button	
        self.fileButton = tk.Button(window, text="Open File...", command=self.clicked) 
        self.fileButton.grid(column=1, row=1)
        
        self.exitButton = tk.Button(window, text="Exit", command=window.destroy) 
        self.exitButton.grid(column=1, row=10)
        
        # Text entry
        self.textSamples = tk.Entry(window,width=10,textvariable=v)
        self.textSamples.grid(column=50, row=1)
        
        self.plotButton = tk.Button(window, text="Plot file", state = 'disabled', command=self.plotit) 
        self.plotButton.grid(column=60, row=1)
        
        # Global variables        
        global x_samples 
        global x
        global y
      
    def clicked (self):
        #subprocess.Popen(r'explorer /select, "C:\Users\Frank Pintor\Desktop\Data analyzer\"')
        tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing     
        self.filename = askopenfilename() # show an "Open"
        
        self.sizeSample = int(v.get())
    
        if (self.filename != ""):
            
            # Open file label changed                
            self.openFileLabel.configure(text="File selected")
            print("File located at: ", self.filename)
            # Reading csv using panda
            df = pd.read_csv(self.filename)    
            self.x = df['Time']
            self.y = df['fmCH[1].I.Rate']
            df = df.append(self.x).append(self.y)
            # Choosing only the last portion of data
            self.x_samples = list(self.x[(len(list(self.x))-self.sizeSample):])
            self.plotButton.config(state="normal")
            
            print("File loaded succesfully")
            print("Sample size selected: ", self.sizeSample)
        else:
            print("File not chosen")

    def plotit (self):
        
        #Is it the first time we draw/plot a graph?
        self.flag = 0
        # Create a subset of random values that will represent the graph
        # Mainly for computation ease
        for i in range(len(self.x_samples)):
            self.x_samples = random.sample(self.x_samples, int(self.sizeSample/2))
        # Check the indexes of those values in the x list
        for t in range(len(self.x_samples)):
            indexes.append(list(self.x).index(self.x_samples[t]))
        # Sort those indexes
        indexes.sort()
        # Update the timeline instead of the one provided by P&G
        for k in range(len(indexes)):
            x_newTime.append(k*timeSample) 
        # Get the values from the y list and bring them back to life
        for j in range(len(indexes)):
            y_samples.append(self.y[indexes[j]])
        
        # Find minimum value - Fastest extraction value
        y_min = [(min(y_samples))] * len(x_newTime)
        
        print("Fastest extraction found: ", y_min[1])        
        # Create figure object
        fig = Figure(figsize=(5,5))
        graph = fig.add_subplot(111)
        
        # Clear graph
        if (self.flag == 1):
            del graph.lines[0]   
        
        # Plot the extraction        
        extractionPlot = graph.plot(x_newTime, y_samples)
        # Plot the Lowest extraction line
        FastestExtraction = graph.plot(x_newTime, y_min, label='Fastest Extraction', linestyle='--')                         
        
        graph.set_title("Extraction Rate for a 30Kg Barrel")
        
        graph.set_ylabel("Flow Rate (g/Sec)")
        graph.set_xlabel("Time (mSec)")
        # Include our graph in the tkinter window and draw it!
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().grid(column=200,row=250)
        canvas.draw()
        
        # Tell the world you have drawn/plotted it!
        self.flag = 1 

# tk standard 
window= tk.Tk()
window.title("Large Pour - Extraction plotter - ARTC")
window.geometry('740x580')

print("Loading...")

# Variables
v = tk.StringVar(window, value='5000')
sizeSample = int(v.get())
timeSample = 10

print("Ready")

start= mclass (window)
window.mainloop()