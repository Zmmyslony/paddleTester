import serial
import vxi11

from auxiliary import makeWorkingDirs
from auxiliary import inputStepNumber
from functions import testPaddle

OSCILLOSCOPE_IP = "10.34.13.126"
ARDUINO_PORT = "/dev/ttyUSB3"
BAUD_RATE = 9600
ARDUINO_TIMEOUT = 0.1


def startTesting(diameter):
    measDir, rotorLogs = makeWorkingDirs(diameter)

    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=ARDUINO_TIMEOUT)
    oscilloscope = vxi11.Instrument(OSCILLOSCOPE_IP)
    oscilloscope.write("CHDR off")  # change display mode

    normalization = [4.24, 4.6]
    qwpSteps, hwpSteps = inputStepNumber()

    testPaddle(oscilloscope, arduino, *normalization, diameter, measDir, rotorLogs,
              qwpSteps=qwpSteps, hwpSteps=hwpSteps, hwp_ch=1, qwp_ch=1)


startTesting(14)
