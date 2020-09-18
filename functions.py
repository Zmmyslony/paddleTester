from arduinoControl import rotatePaddle
from oscilloscopeCommunication import measureVoltage
from auxiliary import countPrefix, makeWorkingDirs, confirmation
import os

BASE_ANGLE = 0


def genMeasurementFilename(diameter, shortName):
    measurementDir = "measurements/{}mm".format(diameter)
    shortName = shortName + "_raw"
    nameSuffix = shortName + str(countPrefix(measurementDir, shortName)) + ".tsv"
    measurementFilename = os.path.join(measurementDir, nameSuffix)
    return measurementFilename


def gen_stokes_filename(diameter, shortName):
    measurementDir = "measurements/{}mm".format(diameter)
    shortName = shortName + "_stokes"
    nameSuffix = shortName + str(countPrefix(measurementDir, shortName)) + ".tsv"
    measurementFilename = os.path.join(measurementDir, nameSuffix)
    return measurementFilename


def writeHeader(file, shortName, longName, steps, sensitivity_ch1, sensitivity_ch2):
    file.write("# {} wave plate rotations. Step: {} degrees \n".format(longName, 180 / steps))
    file.write("# _channel normalization: {} [V]\t{}[V]\n".format(sensitivity_ch1, sensitivity_ch2))
    file.write("# Ver1\tHor1\tVer2\tHor2\tVer3\tHor3\tI1\tI2\tI3\n")


def genNewAngle(currentStep, totalSteps, invert):
    newAngle = BASE_ANGLE
    if totalSteps > 0:
        newAngle = 180 * currentStep / totalSteps
    if invert:
        newAngle = 180 - newAngle
    return newAngle


def movePaddleToStart(arduinoPort, other_ch, invertOther_ch):
    rotatePaddle(arduinoPort, other_ch, genNewAngle(0, 0, invertOther_ch))


def powers_to_stokes(measurements):
    stokes = np.zeros((3, measurements.shape[1]))
    stokes[:, 0] = (measurements[:, 1] - measurements[:, 0]) /
                   (measurements[:, 1] + measurements[:, 0])
    stokes[:, 0] = (measurements[:, 3] - measurements[:, 2]) /
                   (measurements[:, 3] + measurements[:, 2])
    stokes[:, 1] = -(measurements[:, 5] - measurements[:, 4]) /
                   (measurements[:, 5] + measurements[:, 4])
    return stokes


def measure_wave_plate(arduinoPort, oscilloscope, shortName,
              longName, steps, working_ch, other_ch, sensitivity_ch1,
              sensitivity_ch2, diameter, invertWorking_ch=False,
              invertOther_ch=False):
    print(steps)
    if steps > 0:
        measurements = np.zeros((steps + 1), 6)
        print("Measuring " + shortName)

        messages = ("Set HWP and QWP at 0 degrees. (y)\n",
                    "Set HWP at 22.5 and QWP at 0 degrees. (y)\n",
                    "Set HWP at 0 and QWP at 45 degrees. (y)\n")
        error_message = "Set correct angles and confirm with \"y\"!"

        for j in range(3):
            confirmation(messages[i], error_message)
            movePaddleToStart(arduinoPort, other_ch, invertOther_ch)
            for i in range(steps + 1):
                print("\r{} / {}".format(i, steps), end = '')
                newAngle = genNewAngle(i, steps, invertWorking_ch)
                rotatePaddle(arduinoPort, working_ch, newAngle)
                measurements[i, 2*j:2*j+1] = *measureVoltage(oscilloscope, sensitivity_ch1, sensitivity_ch2)

                # measurementFile.write("{}\t{:.3f}\t{:.3f}\n".format(newAngle, *measurements))

        stokes = powers_to_stokes(measurements)
        measurementFilename = genMeasurementFilename(diameter, shortName)
        measurementFile = open(measurementFilename, "w")
        writeHeader(measurementFile, shortName, longName, steps, sensitivity_ch1, sensitivity_ch2)
        measurementFile.close()

        stokes_filename = gen_stokes_filename(diameter, shortName)
        np.savetxt(stokes_filename, stokes, delimiter = "\t", fmt="%.3f")


def testPaddle(oscilloscope, arduinoPort, sensitivity_ch1, sensitivity_ch2,
               diameter, measDir, rotorLogs, qwp_ch=1, hwp_ch=2, qwpSteps=0, hwpSteps=0):
    # makeWorkingDirs(diameter)
    measure_wave_plate(arduinoPort, oscilloscope, "QWP", "Quarter", qwpSteps,
              qwp_ch, hwp_ch, sensitivity_ch1, sensitivity_ch2, diameter,
              invertOther_ch=True)
    measure_wave_plate(arduinoPort, oscilloscope, "HWP", "Half", hwpSteps,
              hwp_ch, qwp_ch, sensitivity_ch1, sensitivity_ch2, diameter,
              invertWorking_ch=True)
