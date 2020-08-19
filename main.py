import serial
import vxi11

from auxiliary import makeWorkingDirs
from auxiliary import inputStepNumber
from measuring import testPaddle

OSCILLOSCOPE_IP = "10.34.13.126"
ARDUINO_PORT = "/dev/ttyUSB1"
BAUD_RATE = 9600
ARDUINO_TIMEOUT = 0.1


def startTesting(diameter):
    measDir, rotorLogs = makeWorkingDirs(diameter)

    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout = ARDUINO_TIMEOUT)
    oscilloscope = vxi11.Instrument(OSCILLOSCOPE_IP)
    oscilloscope.write("CHDR off") # change display mode

    normalization = [3.00, 3.00]
    qwpSteps, hwpSteps = inputStepNumber()
    testPaddle(oscilloscope, arduino, *normalization, qwpSteps, hwpSteps)

startTesting(16)
