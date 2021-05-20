import serial
import time
from time import sleep


ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.5)
data = '0 0\n'
data = bytes(data, encoding='utf-8')
ser.write(data)
ser.close()
time.sleep(2)
