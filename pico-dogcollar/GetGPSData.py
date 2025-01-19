from machine import UART
import time

uart = UART(0, 9600)

def parseLine(raw_line):
    if raw_line:
        try:
            raw_line = raw_line.decode("utf-8").strip()
            line = raw_line.split(',')
            if line[0].startswith('$'):
                return line, True
            else:
                return "", False
        except Exception as e:
            return "", False
    else:
        return "", False

while True:
    raw_line = uart.readline()
    line, truth = parseLine(raw_line)
    if not truth:
        continue
    if(line[0] in ["$GNGGA", "$GNGLL", "$GNRMC"]):
        print(line)
    time.sleep(0.1)
