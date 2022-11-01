import pyvisa
import time
import os
from Setting import *

filepath = "/home/keti-kvm/DATA/mesured_data.csv"

F_start = 2.39 # start frequency in GHz
F_stop = 2.41 # stop frequency in GHz
F_cent = 2.4
F_nump = 500 # number o ffrequency points in a sweep
BWIF = 10000.0 # IF bandwidth in Hz
IF_sel = 'HIGH' # selectivity of IF receiver: NOR | MID | GIH
POWER = -30 # RF source power in dBm
AVER_num = 3 # number of frequency sweeps used to average a trace
AVER_mode = 'RED'  # AUTO/FLATten/REDuce/MOVing different averaging modes
AVER_state = 'ON'  # Averaging ON/OFF
VNA_timeout = 10000.0  # VNA's timeout (ms) should be sufficiently large to allow long operations


#contect to VNA
rm = pyvisa. ResourceManager()
VNA = rm.open_resource('PCTIP:169.254.250.133::INSTR')
print(VNA.query('*IDN?')) # IDNUMBER

#VNA.write("INIT:CONT OFF")
#VNA.write("INIT")
#VNA.query("*OPC?") # Operation Complete

#Check the error queue
print(VNA.query("SYST:ERR?"))

#Select the default measurement name as assigned on preset
#  VNA.write("CALC:PAR:SEL 'CH1Tr1'")
#Create channel 4 and a trace named Ch4Tr1 to measure the input reflection coeffcient S12.
VNA.write("CALC:PAR:SDEF 'Ch4Tr1', 'S12'")
VNA.write("CALC:PAR:SEL 'Trc1'; CALC1:MARK ON")
VNA.write("CALC:PAR:SDEF 'Ch4Tr2', 'S12'")

#Set data transfer format to REAL
VNA.write("FORM:DATA REAL, 32")

# Data
Tr1_data = []
Tr2_data = []

#The SDATA assertion queries underlying real and imaginary pair data
VNA.write("CALC:DATA? FDAT")
VNA.write("CALC4:FORM PHAS; :DISP:WIND:TRAC2:FEED 'CH4TR1'")
TR1_data = VNA.read()

#check system error
print(VNA.query("SYST:ERR?"))

#close the cisa connection
VNA.close()


#Run the test
phase_Measured = float(VNA.query("CALC:PAR:MEAS? 'Ch1Tr1'"))
power_Measured = float(VNA.query("CALC:PAR:MEAS? 'Ch1Tr2'"))

# Controll Pin
GPIO.output(P_or_S, GPIO.LOW)
GPIO.output(OPT, GPIO.LOW)
print("Start to control GPIO")
for PIN_HIGH_P in range(0, 6, 1):
    #print(PIN_HIGH_P)    
    if PIN_HIGH_P == 0:
        PIN_HIGH_P = 22
    elif PIN_HIGH_P == 1:
        PIN_HIGH_P = 10
    elif PIN_HIGH_P == 2:
        PIN_HIGH_P = 9
    elif PIN_HIGH_P == 3:
        PIN_HIGH_P = 11
    elif PIN_HIGH_P == 4:
        PIN_HIGH_P = 0     
    elif PIN_HIGH_P == 5:
        PIN_HIGH_P = 5
    elif PIN_HIGH_P == 6:
        PIN_HIGH_P = 6
    elif PIN_HIGH_P == 7:
        PIN_HIGH_P = 13
        
    for PIN_HIGH_A in range(0, 6, 1):
        #print(PIN_HIGH_A)  
        if PIN_HIGH_A == 0:
            PIN_HIGH_A = 14
        elif PIN_HIGH_A == 1:
            PIN_HIGH_A = 15
        elif PIN_HIGH_A == 2:
            PIN_HIGH_A = 18
        elif PIN_HIGH_A == 3:
            PIN_HIGH_A = 23
        elif PIN_HIGH_A == 4:
            PIN_HIGH_A = 24
        elif PIN_HIGH_A == 5:
            PIN_HIGH_A = 25
        elif PIN_HIGH_A == 6:
            PIN_HIGH_A = 8
        
        time.sleep(5)
        for pin in pins_P:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        for pin in pins_A:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            
        GPIO.output(PIN_HIGH_P, GPIO.HIGH)
        GPIO.output(PIN_HIGH_A, GPIO.HIGH)
        print("GPIO "+str(PIN_HIGH_P)+" & "+str(PIN_HIGH_A)+" set HIGH")

        
        #Write results to a file
        with open(filepath, "a") as file:
            if os.stat(filepath).st_size == 0: #if empty file, wrute a nice header
                file.write("Setpoint [Deg], [dB], Measured [Deg], [dB]\n")
            file.write("{}, {}, {:12.2f}, {:13.2f}\n".format(PIN_HIGH_P, PIN_HIGH_A, phase_Measured, power_Measured))
        file.close()


