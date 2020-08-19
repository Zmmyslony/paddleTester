import time
from auxiliary import currentTime

REFRESH_PERIOD = 0.01
ROTOR_PORT = "/dev/ttyUSB1"
FULL_ROTATION = 360
HALF_ROTATION = 180


# file = open(filename, "w")
# rotor = serial.Serial(ROTOR_PORT, 9600, timeout = 0.1)


def writeCommand(file, instrument, command):
    syntaxedCommand = "#" + command + "\r"
    instrument.write(syntaxedCommand)
    response = instrument.read()
    while not response:
        time.sleep(REFRESH_PERIOD)
        response = instrument.read()
    file.write(currentTime + "\t" + response)
    return response


def writeNonzeroCommand(file, instrument, command, val):
    if not val == 0:
        command = command + str(int(val))
        writeCommand(file, instrument, command)


def inRange(val, lowerLimit, upperLimit):
    if val > upperLimit:
        return upperLimit
    elif val > lowerLimit:
        return val
    else:
        return lowerLimit


def coerce(val):
    val = val % FULL_ROTATION
    if val >= HALF_ROTATION:
        return val - FULL_ROTATION
    else:
        return val


def invert(val, switch):
    if switch:
        return -val
    else:
        return val


def angleToSteps(angle, stepsPerRev, microsteps):
    angle = angle / FULL_ROTATION
    stepPrecision = stepsPerRev * microsteps
    steps = int(round(angle * stepPrecision))
    correctedAngle = steps / stepPrecision
    return steps, correctedAngle


def getShortestPath(newVal, oldVal):
    moveVal = coerce(newVal)
    moveVal = (moveVal - oldVal) % FULL_ROTATION
    if FULL_ROTATION - moveVal < moveVal:
        return FULL_ROTATION - moveVal
    else:
        return moveVal


# def setAccelerationRamp(file, rotor, acceleration):
#     command = "b" + str(acceleration)
#     writeCommand(file, rotor, command)


def setMicrostepping(file, rotor, microsteps):
    command = "g" + str(microsteps)
    writeCommand(file, rotor, command)


def setMode(file, instrument, mode, subMode):
    command = "!" + str(mode)
    subCommand = "p" + str(subMode)
    writeCommand(file, instrument, command)
    writeCommand(file, instrument, subCommand)


def setCurrentLimit(file, instrument, phaseCurrent, phaseCurrentAtStandstill, modeAbsolute):
    if modeAbsolute:
        limiter = 0.7 * 0.01
    else:
        limiter = 1
    phaseCurrent = phaseCurrent / limiter
    phaseCurrentAtStandstill = phaseCurrentAtStandstill / limiter

    phaseCurrent = inRange(phaseCurrent, 0, 100)
    phaseCurrentAtStandstill = inRange(phaseCurrentAtStandstill, 0, 100)

    commandCurrent = "i" + str(int(phaseCurrent))
    commandCurrentStandstill = "r" + str(int(phaseCurrentAtStandstill))

    writeCommand(file, instrument, commandCurrent)
    writeCommand(file, instrument, commandCurrentStandstill)


def setAccelerationRamp(file, instrument, startSpeed, maxSpeed, acceleration,
                        stepsPerRev, microsteps, degPerS):
    stepPrecision = stepsPerRev * microsteps
    if degPerS:
        stepPrecision = stepPrecision / FULL_ROTATION
    writeNonzeroCommand(file, instrument, "u", inRange(startSpeed * stepPrecision, 0, 160000))
    writeNonzeroCommand(file, instrument, "o", inRange(maxSpeed * stepPrecision, 0, 1000000))
    writeNonzeroCommand(file, instrument, "b", inRange(acceleration * stepPrecision, 0, 65535))


def startMotor(file, instrument):
    writeCommand(file, instrument, "A")


def setTravelDirection(file, instrument, intAngle):
    if intAngle > 0:
        writeCommand(file, instrument, "d1")
    else:
        writeCommand(file, instrument, "d0")


def setTravelDistance(file, instrument, intAngle):
    intAngle = abs(intAngle)
    command = "s{:03d}".format(intAngle)
    writeCommand(file, instrument, command)


def moveDegrees(file, instrument, angle, stepsPerRev, microsteps):
    steps, correctedAngle = angleToSteps(angle, stepsPerRev, microsteps)
    if not steps == 0:
        setTravelDirection(file, instrument, steps)
        setTravelDistance(file, instrument, steps)
        startMotor(file, instrument)
    return correctedAngle


def getPosition(file, instrument, stepsPerRev, microsteps):
    readout = writeCommand(file, instrument, "C")
    position = int(readout[2:])
    stepPrecision = stepsPerRev * microsteps / FULL_ROTATION
    absolutePosition = position / stepPrecision
    return absolutePosition


def initRotor(file, rotor, microsteps, mode, subMode,
              phaseCurrent, phaseCurrentAtStandstill, modeAbsolute, startSpeed,
              maxSpeed, acceleration, stepsPerRev, degPerS):
    # setAccelerationRamp(file, rotor, acceleration)
    setMicrostepping(file, rotor, microsteps)
    setMode(file, rotor, mode, subMode)
    setCurrentLimit(file, rotor, phaseCurrent, phaseCurrentAtStandstill, modeAbsolute)
    setAccelerationRamp(file, rotor, startSpeed, maxSpeed, acceleration,
                        stepsPerRev, microsteps, degPerS)
