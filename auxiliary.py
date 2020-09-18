import os
from datetime import datetime

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
    # print("Insert the number of angles of quarter wave plate to be measured: ")
    qwpSteps = int(input("Insert the number of angles of quarter wave plate to be measured: ""))
    # print("\nInsert the number of angles of half wave plate to be measured: ")
    hwpSteps = int(input("Insert the number of angles of half wave plate to be measured: "))
    return qwpSteps, hwpSteps


def countPrefix(directory, prefix):
    i = 0
    for file in os.listdir(directory):
        if file.startswith(prefix):
            i += 1
    return i + 1

def confirmation(message, error_message):
    keystroke = input(message)
    while(not keystroke = y):
        print(error_message)
        keystroke = input(message)
    return keystroke
