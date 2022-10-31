import pyvisa
import time
import os
import Setting

#contect to VNA
rm = pyvisa. ResourceManager()
VNA = rm.open_resource('PCTIP:169.254.250.133::INSTR')


#set freq and power
VNA.write("SOUR:FREQ 2.4GHz")
VNA.write("SOUR:POW -30dBm")

VNA.query("SOUR:FREQ?", "SOUR:POW?")

#start and stop send signal
VNA.write("OUTP ON")
sleep(10)
VNA.write("OUTP OFF")
VNA.query("OUTP?")

n=0
while n < 7:
    