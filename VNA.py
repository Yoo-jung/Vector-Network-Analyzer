import pyvisa
import time
import os

filepath = "./data.csv"

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
#Set tiem out - 10 Seconds
VNA.timeout = 10000

VNA.write("*RST") # Reset
VNA.write("*CLS") # Clear Status

print(VNA.query('*IDN?')) # IDNUMBER

VNA.write("INIT:CONT OFF")
VNA.write("INIT")
VNA.query("*OPC?") # Operation Complete

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
phase = 0
while phase <= 7:
    VNA.write()
    sleep(2)
    phase_Measured = float('')
    
    #Write results to a file
    with open(filepath, "a") as file:
        if os.stat(filepath).st_size == 0: #if empty file, wrute a nice header
            file.write("Setpoint [Deg], [dB], Measured [Deg], [dB]\n")
        file.write("{:12.2f}, {:13.2f}\n".format(phase, phase_Measured))
    file.close()
    
    phase += 1




