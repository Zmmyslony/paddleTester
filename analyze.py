import tkinter as tk
import numpy as np
from tkinter import filedialog


# def analyze(measurementDir, stokesDir):
def analyze(measurementDir):
    root = tk.Tk()
    root.withdraw()

    firstFile = filedialog.askopenfilename(initialdir=measurementDir)
    secondFile = filedialog.askopenfilename(initialdir=measurementDir)
    thirdFile = filedialog.askopenfilename(initialdir=measurementDir)

    dataI1 = np.genfromtxt(firstFile)
    dataI2 = np.genfromtxt(secondFile)
    dataI3 = np.genfromtxt(thirdFile)

    data = np.hstack((dataI1[:, 1:3], dataI2[:, 1:3], dataI3[:, 1:3]))

    # outputFilename = filedialog.asksaveasfilename(initialdir=stokesDir)
    outputFilename = filedialog.asksaveasfilename()
    np.savetxt(outputFilename, data, delimiter="\t", newline="\n",
               fmt="%.2f")

analyze("../output/2020-09-08/measurements")
