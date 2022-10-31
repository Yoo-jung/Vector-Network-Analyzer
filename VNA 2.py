from dataclasses import dataclass
import pyvisa
import os
from Setting import *

# contect to VNA
# ------------------------------------------------
rm = pyvisa. ResourceManager()
VNA = rm.open_resource('PCTIP:169.254.250.133::INSTR')
VNA.write("*RST") # Reset
VNA.write("*CLS") # Clear Status
print(VNA.query('*IDN?')) # IDNUMBER
# ------------------------------------------------

# set freq and power
# ------------------------------------------------
#VNA.write("SOUR:FREQ1:CW 2.4GHz")
VNA.write("SOUR:FREQ 2.4GHz")
VNA.write("SOUR:POW -30dBm")

VNA.query("SOUR:FREQ?", "SOUR:POW?")
# ------------------------------------------------

# Setting Trace and Check result on screen.
# ------------------------------------------------
# Reset the instrument, creating the default trace Trc1 in channel 1.
# The defualt measured quantity is the forward transmission S21, and defalt format is dB Mag.
VNA.write("*RST")
# Create a second trace in channel 1, assinge the format Phase, and display the new trace in the same diagram.
VNA.write("CLAC:PARR:SDER 'Trc2', 's21'")
# the frace is referenced by the channel 1 suffix 1
VNA.write("CALC:MARK:DEF:FORM PHAS") # Phase
# display the second trace
VNA.write("DISP:WIND:TRAC2:FEED 'Trc2'")
VNA.write("SYST:DISP:UPD ONCE") # GO to local
#remove from the first area.
#VNA.write("DISP:WIND2:STAT ON")
#VNA.write("DISP:WIND2:TRAC2:FEED 'Trc2'")
#VNA.write("DISP:WIND1:TRAC2:DEL") # Trc2 is displayed in both diagrams
# ------------------------------------------------

# Marker setting and Define and display a 
# ------------------------------------------------
VNA.write("SENS1:FREQ:STAR 2.39GHz; STOP 2.41 GHZ")
VNA.write("DISPlay:WINDow1:TRACe1:Y:SCALe:AUTO ONCE")
VNA.write("DISPlay:WINDow1:TRACe2:Y:SCALe:AUTO ONCE")

# ------------------------------------------------

# start and stop send signal
# ------------------------------------------------
VNA.write("OUTP ON")
time.sleep(10)
VNA.write("OUTP OFF")
VNA.query("OUTP?")
# ------------------------------------------------

# Calculate data
# ------------------------------------------------
VNA.write("CALC:MARK:DEF:FORM MLOG") # dB Mag
VNA.write("CALC:DATA? FDAT") # Read the formatted trace data

#Set data transfer format to REAL
VNA.write("FORM:DATA REAL, 32")
# ------------------------------------------------

# Control GPIO pins
# ------------------------------------------------
n=0
print("Start to control GPIO")
while n < 7:
    GPIO.output(PS, GPIO.HIGH)
    for PW in (0, 6, 1):
        GPIO.setup(PW, GPIO.OUT, initial=GPIO.LOW)
        print(PS, PW)
        #여기서 측정?
    print("Done.")
    n += 1
# ------------------------------------------------

# ------------------------------------------------
#check system error
print(VNA.query("SYST:ERR?"))
# ------------------------------------------------

# Save / load the cal files 
# ------------------------------------------------
# C:\Users\Public\Documents\Rohde-Schwarz\Vna\Calibration\Data
# The filename in the folloing two commands must not contain the path
VNA.write("MMEMORY:STORE:CORR 1, 'OSM1 TOSM12.cal'")
# load cal file from calivration file pool
VNA.write("MMEMORY:LOADLCORR 1, 'OSM1 TOSM12.cal'")
# ------------------------------------------------
