import pyvisa
import time
import os

#contect to VNA
rm = pyvisa. ResourceManager()
VNA = rm.open_resource('PCTIP:169.254.250.133::INSTR')

#for touchstone file
channel = 1
ports_string = "1,2"
touchstone_filename = "ch1_data.s4p"

# For trace data
trace_name          = "Trc1"
trace_filename      = "Trc1.csv"

# Indicate which ports you want to
# capture data for before starting sweep
# Note: This must be done for each channel
# Using channel 1 for illustrative purposes:
channel = 1
scpi         = ":CALC{0}:PAR:DEF:SGR {1}"
scpi         = scpi.format(channel, ports_string)
VNA.write(scpi)

# Enable manual sweep mode
# (i.e. control timing)
VNA.write("INIT:CONT:ALL 0")

# Start all sweeps
VNA.write("INIT:SCOP ALL")
VNA.write("INIT")

# Wait for sweeps to finish
# Note: Make sure timeout is long
#       enough for sweeps to complete
VNA.query("*OPC?")

# Save touchstone file to VNA
# Complex formats are:
# - COMP (Re, Im)
# - LINP (Linear magnitude,   phase [deg])
# - LOGP (Log magnitude [dB], phase [deg])
complex_format = "COMP"
scpi = ":MMEM:STOR:TRAC:PORT {0},'{1}',{2},{3}"
scpi = scpi.format(channel, 'temp.s4p', complex_format, ports_string)
VNA.write(scpi)

# Save trace data to VNA as
# displayed on screen
# Note: See command documentation for
#       additional data format options
scpi = ":MMEM:STOR:TRAC '{0}', '{1}', FORM"
scpi = scpi.format(trace_name, 'temp.csv')
VNA.write(scpi)

# Wait for saves to complete
VNA.query("*OPC?")

# Transfer files from VNA
# - See read_file.py
VNA.file.download_file("temp.s4p", touchstone_filename)
VNA.file.download_file("temp.csv", trace_filename)

# Delete files from VNA
VNA.file.delete("temp.s4p")
VNA.file.delete("temp.csv")

VNA.close()