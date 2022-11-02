import pyvisa
import time
import os
from Setting import *

#contect to VNA
rm = pyvisa. ResourceManager()
VNA = rm.open_resource('TCPIP::169.254.250.133::INSTR')
print(VNA.query('*IDN?')) # IDNUMBER
time.sleep(1)
filepath = "./mesured_data.csv"

#check system error
print(VNA.query("SYST:ERR?"))
time.sleep(1)

#-----------------------------------------------
# Setting GPIO Pin
# reset
# Set GPIO mode - 회로의 GPIO 번호 사용
GPIO.setmode(GPIO.BCM)
GPIO.setup(P_or_S, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(OPT, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LE, GPIO.OUT, initial=GPIO.HIGH)

for pin in pins_P:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
for pin in pins_A:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
print("Initial setup complete")
time.sleep(1)

# Controll Pin Loop
GPIO.output(P_or_S, GPIO.LOW)
GPIO.output(OPT, GPIO.LOW)
GPIO.setup(LE, GPIO.LOW)

print("Start to control GPIO")
for PIN_HIGH_P in range(0, 8, 1):
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
        
    for PIN_HIGH_A in range(0, 7, 1):
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
        
        time.sleep(0.5)
        for pin in pins_P:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        for pin in pins_A:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        
        
        GPIO.output(PIN_HIGH_P, GPIO.HIGH)
        GPIO.output(PIN_HIGH_A, GPIO.HIGH)      
        if PIN_HIGH_P == 6:
            GPIO.output(19, GPIO.HIGH)
        else:
            GPIO.output(19, GPIO.LOW)
            
        print("GPIO "+str(PIN_HIGH_P)+" & "+str(PIN_HIGH_A)+" set HIGH")
        
        # Read data
        time.sleep(0.5)
        Measured = float(VNA.query(":CALC:MARK:Y?"))
        time.sleep(0.5)
        #Write results to a file
        with open(filepath, "a") as file:
            if os.stat(filepath).st_size == 0: #if empty file, wrute a nice header
                file.write("Setpoint [Deg], [dB], Measured\n")
            file.write("{}, {}, {:12.2f}\n".format(PIN_HIGH_P, PIN_HIGH_A, Measured))
        file.close()
