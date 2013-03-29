import time
import subprocess
import serial
import processBlink

def initserial():
    s = serial.Serial()
    s.port = "/dev/tty.usbserial-AH01KXWW"
    s.baudrate = 115200
    s.open()
    return s

def broadcast(data):
    """ Helper functions to broadcast to serial port""" 
    s.write(bytes(data))

proc = subprocess.Popen("analyze.out", shell = True, stdout = subprocess.PIPE)

s = initserial()
poor = False
SAMPLE_LEN = 10
direction = 'L'
sProcessor = processBlink(SAMPLE_LEN, 200) #signal processor
duration = 10 #hardcoded duration

while True:
    line = proc.stdout.readline()
    if line != '':
        signal = line.split(": ")
        if signal[0] == "POOR_SIGNAL":
            if int(signal[1]) == 200:
                poor = True
            else:
                poor = False
            print(line)
        elif poor:
            continue
        if signal[0] == "RAW":
            rsp = sProcessor(signal[1])
            if (rsp == 1):
                direction = 'R' if direction == 'L' else 'L' #toggle direction
                broadcast(direction) #Send command through serial
        elif signal[0] == "MEDITATION":
            if int(signal[1]) > 55:
                # move forward
                broadcast("F")
            else:
                # stop
                broadcast("S")
            print(line)
        else:
            print(line)