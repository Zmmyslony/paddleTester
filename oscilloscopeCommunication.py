import vxi11
import time

DELAY_PERIOD = 0.5 #seconds

def askMaxVoltage(oscilloscope, channel):
    response = oscilloscope.ask("C{}:PAVA? MAX".format(channel))
    voltage = float(response[4:-3])
    return voltage

def autoSetup(oscilloscope):
    oscilloscope.write("ASET")

def measureVoltage(oscilloscope, sensitivityCH1, sensitivityCH2):
    autoSetup(oscilloscope)
    time.sleep(DELAY_PERIOD)

    voltageCH1 = askMaxVoltage(oscilloscope, 2) / sensitivityCH1
    voltageCH1 = askMaxVoltage(oscilloscope, 3) / sensitivityCH2
    return voltageCH1, voltageCH2
