import serial

data = serial.Serial('com8', 9600)

while True:
    if data.inWaiting() > 0:
        print data.readline()