from datetime import datetime
from arduinoControl import rotatePaddle
from oscilloscopeCommunication import measureVoltage

BASE_ANGLE = 0


def testPaddle(oscilloscope, arduino, ch1Normalization, ch2Normalization, qwpSteps, hwpSteps,
               measDir, rotorLogs, qwpChannel=1, hwpChannel=2):
    timeStamp = datetime.now()
    timeStamp = timeStamp.strftime("%Y-%b-%d_%H:%M")

    if qwpSteps > 0:
        print("Measuring QWP")
        filenameQWP = "measurements/{}_{}_{}.csv".format(timeStamp, qwpSteps, "QWP")
        fileQWP = open(filenameQWP, "w")
        fileQWP.write("# Quarter wave plate rotations. Step: {} degrees \n".format(180 / qwpSteps))
        fileQWP.write("# Channel normalization: {} [V]\t{}[V]\n".format(ch1Normalization, ch2Normalization))
        fileQWP.write("# QWP\tHWP\tVer\tHor\n")
        rotatePaddle(arduino, hwpChannel, 180 - BASE_ANGLE)
        for i in range(qwpSteps + 1):
            newQwpAngle = 180 / qwpSteps * i
            rotatePaddle(arduino, qwpChannel, newQwpAngle)
            measurements = measureVoltage(oscilloscope, ch1Normalization, ch2Normalization)
            fileQWP.write("{}\t{}\t{:.3f}\t{:.3f}\n".format(newQwpAngle, BASE_ANGLE,
                                                            *measurements))
        fileQWP.close()

    if hwpSteps > 0:
        print("Measuring HWP")
        filenameHWP = "measurements/{}_{}_{}.csv".format(timeStamp, hwpSteps, "HWP")
        fileHWP = open(filenameHWP, "w")
        fileHWP.write("# Half wave plate rotations. Step: {} degrees \n".format(180 / hwpSteps))
        fileHWP.write("# Channel normalization: {} [V]\t{}[V]\n".format(ch1Normalization, ch2Normalization))
        fileHWP.write("# QWP\tHWP\tVer\tHor\n")
        rotatePaddle(arduino, qwpChannel, BASE_ANGLE)
        for i in range(hwpSteps + 1):
            newHwpAngle = 180 - 180 / hwpSteps * i
            rotatePaddle(arduino, hwpChannel, newHwpAngle)
            measurements = measureVoltage(oscilloscope, ch1Normalization, ch2Normalization)
            fileHWP.write("{}\t{}\t{:.3f}\t{:.3f}\n".format(BASE_ANGLE, newHwpAngle,
                                                            *measurements))
        fileHWP.close()
