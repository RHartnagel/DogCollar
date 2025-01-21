from machine import UART
import struct
import time

uart = UART(0, 9600)

def filterLines(raw_line):
    if raw_line:
        try:
            raw_line = raw_line.decode("utf-8").strip()
            line = raw_line.split(',')
            if(line[0] in ["$GNGGA", "$GNGLL", "$GNRMC"] and len(line) > 6):
                return line, True
            else:
                return "", False
        except Exception as e:
            return "", False
    else:
        return "", False

def convertLat(rawLat, dir):
    print()        

def convertLong(rawLong, dir):
    print()     

def convertTime(rawTime):
    print()     

def parseLine(lines):
    if lines[0] == "$GNGGA" and all(lines[i] for i in [1, 2, 3, 4, 5]):
        print(f"Time: {lines[1]}, Lat: {lines[2]} {lines[3]}, Long: {lines[4]} {lines[5]}")
    elif lines[0] == "$GNGLL" and all(lines[i] for i in [1, 2, 3, 4, 5]):
        print(f"Time: {lines[5]}, Lat: {lines[1]} {lines[2]}, Long: {lines[3]} {lines[4]}")
    elif lines[0] == "$GNRMC" and all(lines[i] for i in [1, 3, 4, 5, 6]):
            print(f"Time: {lines[1]}, Lat: {lines[3]} {lines[4]}, Long: {lines[5]} {lines[6]}")
    else:
        raise Exception("Bad Input/Warming Up")

def createSendPacket(lat, long):
    sendLat = int(lat * 1e5)
    sendLong = int(long * 1e5)
    timeNow = int(time.time())
    return struct.pack("!iiI", sendLat, sendLat, int(timeNow))

while True:
    time.sleep(0.1)
    raw_line = uart.readline()
    message, truth = filterLines(raw_line)
    if not truth:
        continue
    try:
        parseLine(message)
    except Exception as e:
        print(f"got error: {e}")
        continue
