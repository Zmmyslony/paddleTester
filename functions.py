from arduinoControl import rotatePaddle
from oscilloscopeCommunication import measureVoltage
from auxiliary import countPrefix, makeWorkingDirs
import os

BASE_ANGLE = 0


def genMeasurementFilename(diameter, shortName):
    measurementDir = "measurements/{}mm".format(diameter)
    nameSuffix = shortName + str(countPrefix(measurementDir, shortName)) + ".tsv"
    measurementFilename = os.path.join(measurementDir, nameSuffix)
    return measurementFilename


def writeHeader(file, shortName, longName, steps, sensitivityCH1, sensitivityCH2):
    file.write("# {} wave plate rotations. Step: {} degrees \n".format(longName, 180 / steps))
    file.write("# Channel normalization: {} [V]\t{}[V]\n".format(sensitivityCH1, sensitivityCH2))
    file.write("# {}\tVer\tHor\n".format(shortName))


def genNewAngle(currentStep, totalSteps, invert):
    newAngle = BASE_ANGLE
    if totalSteps > 0:
        newAngle = 180 * currentStep / totalSteps
    if invert:
        newAngle = 180 - newAngle
    return newAngle


def movePaddleToStart(arduinoPort, otherCH, invertOtherCH):
    rotatePaddle(arduinoPort, otherCH, genNewAngle(0, 0, invertOtherCH))


def measureWP(arduinoPort, oscilloscope, shortName,
              longName, steps, workingCH, otherCH, sensitivityCH1,
              sensitivityCH2, diameter, invertWorkingCH=False,
              invertOtherCH=False):
    print(steps)
    if steps > 0:
        measurementFilename = genMeasurementFilename(diameter, shortName)
        measurementFile = open(measurementFilename, "w")

        print("Measuring " + shortName)
        writeHeader(measurementFile, shortName, longName, steps, sensitivityCH1, sensitivityCH2)
        movePaddleToStart(arduinoPort, otherCH, invertOtherCH)
        for i in range(steps + 1):
            print("\r{} / {}".format(i, steps), end = '')
            newAngle = genNewAngle(i, steps, invertWorkingCH)
            rotatePaddle(arduinoPort, workingCH, newAngle)
            measurements = measureVoltage(oscilloscope, sensitivityCH1, sensitivityCH2)
            measurementFile.write("{}\t{:.3f}\t{:.3f}\n".format(newAngle, *measurements))
        measurementFile.close()


def testPaddle(oscilloscope, arduinoPort, sensitivityCH1, sensitivityCH2,
               diameter, measDir, rotorLogs, qwpCH=1, hwpCH=2, qwpSteps=0, hwpSteps=0):
    # makeWorkingDirs(diameter)
    measureWP(arduinoPort, oscilloscope, "QWP", "Quarter", qwpSteps,
              qwpCH, hwpCH, sensitivityCH1, sensitivityCH2, diameter,
              invertOtherCH=True)
    measureWP(arduinoPort, oscilloscope, "HWP", "Half", hwpSteps,
              hwpCH, qwpCH, sensitivityCH1, sensitivityCH2, diameter,
              invertWorkingCH=True)
