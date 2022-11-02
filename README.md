# Vector-Network-Analyzer
## automated measuring system

VNA : https://www.rohde-schwarz.com/us/products/test-and-measurement/network-analyzers/rs-znd-vector-network-analyzers_63493-65409.html
DIgital Phase Shifter : PE43711
Digital Step Attenuator : PE44820

Connect to Vector Network Analyzer use TCP/IP and pyvisa.
Control VNA code  with "https://github.com/Yoo-jung/PE43711-PE44820'
for automated measuring system.

Action details:
% connnect to VNA
% print IDN
% remote GPIO pin to controll DPS, DSA.
% read the data(dB and phase)
% save the data
% done
