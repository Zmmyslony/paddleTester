import time

REFRESH_INTERVAL = 0.05


def writeCommand(port, command):
    port.write(command.encode())
    data = port.readline()[:-2]
    while not data:
        data = port.readline()[:-2]
        time.sleep(REFRESH_INTERVAL)
    return str(data)


def rotationCommand(channel, angle):
    return "ch{:1} {}".format(channel, angle)


def rotatePaddle(arduino, channel, angle):
    writeCommand(arduino, rotationCommand(channel, angle))
