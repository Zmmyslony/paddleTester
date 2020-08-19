import os
from datetime import datetime
import glob

OUTPUT_DIRECTORY = "../output"

def makeDir(dirPath):
    if not os.path.isdir(dirPath):
        os.makedirs(dirPath)

def currentTime():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def currentDate():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

def makeWorkingDirs(diameter):
    date = currentDate()
    outputDir = os.path.join(OUTPUT_DIRECTORY, date)
    makeDir(outputDir)
    os.chdir(outputDir)
    measurementsDir = "measurements/" + str(diameter) + "mm/"
    rotorOutputDir = "logs/rotor/"
    makeDir(rotorOutputDir)
    makeDir(measurementsDir)
    return measurementsDir, rotorOutputDir

def inputStepNumber():
    print("Insert the number of angles of quarter wave plate to be measured: ")
    qwpSteps = input()
    print("\nInsert the number of angles of half wave plate to be measured: ")
    hwpSteps = input()
    return qwpSteps, hwpSteps
