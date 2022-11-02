import pyvisa

#contect to VNA
rm = pyvisa. ResourceManager()
VNA = rm.open_resource('TCPIP::169.254.250.133::INSTR')
print(VNA.query('*IDN?')) # IDNUMBER