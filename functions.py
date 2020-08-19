from datetime import datetime
from arduinoControl import rotatePaddle
from oscilloscopeCommunication import measureVoltage
import os

BASE_ANGLE = 0

def generateFilenamePrefix():
    timeStamp = datetime.now()
    date = timeStamp.strftime("%Y-%b-%d")
    if not os.path.isdir("measurements/" + date):
        os.mkdir("measurements/" + date)
    currentTime = timeStamp.strftime("%H:%M")
    filenamePrefix = "measurements/" + date + "/" + currentTime
    return filenamePrefix

def testPaddle(oscilloscope, arduino, sensitivityCH1, sensitivityCH2,
 qwpCH = 1, hwpCH = 2, qwpSteps = 0, hwpSteps = 0):
    filenamePrefix = generateFilenamePrefix()

    measureWP(arduino, oscilloscope, filenamePrefix, "QWP", "Quarter", qwpSteps,
             qwpCH, hwpCH, sensitivityCH1, sensitivityCH2, invertOtherCH = True)
    measureWP(arduino, oscilloscope, filenamePrefix, "HWP", "Half", hwpSteps,
             hwpCH, qwpCH, sensitivityCH1, sensitivityCH2, invertWorkingCH = True)

def measureWP(arduino, oscilloscope, filenamePrefix, shortName,
             longName, steps, workingCH, otherCH, sensitivityCH1,
             sensitivityCH2, invertWorkingCH = False, invertOtherCH = False):
    if(steps > 0):
        print("Measuring " + shortName)
        filename = filenamePrefix + "_{}_{}.tsv".format(steps, shortName)
        file = open(filename, "w")
        writeHeader(file, shortName, longName, steps, sensitivityCH1, sensitivityCH2)
        movePaddleToStart(arduino, otherCH, invertOtherCH)
        for i in range(steps + 1):
            newAngle = genNewAngle(i, steps, invertWorkingCH)
            rotatePaddle(arduino, workingCH, newAngle)
            measurements = measureVoltage(oscilloscope, sensitivityCH1, sensitivityCH2)
            file.write("{}\t{:.3f}\t{:.3f}\n".format(newAngle, *measurements))
        file.close()

def genNewAngle(currentStep, totalSteps, invert):
    newAngle = BASE_ANGLE
    if totalSteps > 0:
        newAngle = 180 * currentStep / totalSteps
    if invert:
        newAngle = 180 - newAngle
    return newAngle

def movePaddleToStart(arduino, otherCH, invertOtherCH):
    rotatePaddle(arduino, otherCH, genNewAngle(0, 0, invertOtherCH))

def writeHeader(file, shortName, longName, steps, sensitivityCH1, sensitivityCH2):
    file.write("# {} wave plate rotations. Step: {} degrees \n".format(waveplateNameLong, 180 / steps))
    file.write("# Channel normalization: {} [V]\t{}[V]\n".format(sensitivityCH1, sensitivityCH2))
    file.write("# {}\tVer\tHor\n".format(waveplateNameShort))
