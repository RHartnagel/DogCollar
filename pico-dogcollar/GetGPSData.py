from machine import UART
import struct
import time

uart = UART(0, 9600)

def format(value, fmt):
    if fmt.endswith('b'):  # Handle binary formatting
        bit_length = int(fmt[:-1])
        binary_str = bin(value)[2:]
        return '0' * (bit_length - len(binary_str)) + binary_str
    else:
        raise ValueError(f"Unsupported format: {fmt}")

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

def parseLine(lines):
    if lines[0] == "$GNGGA" and all(lines[i] for i in [1, 2, 3, 4, 5]):
        info = LocationInfo(lines[1], lines[2], lines[3], lines[4], lines[5])
        return info
    elif lines[0] == "$GNGLL" and all(lines[i] for i in [1, 2, 3, 4, 5]):
        info = LocationInfo(lines[5], lines[1], lines[2], lines[3], lines[4])
        return info
    elif lines[0] == "$GNRMC" and all(lines[i] for i in [1, 3, 4, 5, 6]):
        info = LocationInfo(lines[1], lines[3], lines[4], lines[5], lines[6])
        return info
    else:
        raise Exception("Bad Input/Warming Up")

def createSendPacket(lat, long):
    sendLat = int(lat * 1e5)
    sendLong = int(long * 1e5)
    timeNow = int(time.time())
    return struct.pack("!iiI", sendLat, sendLong, int(timeNow))

class LocationInfo:
    def __init__(self, time, lat, dLat, long, dLong):
        self.rawTime = time
        self.rawLat = lat
        self.rawLong = long
        self.dLat = dLat
        self.dLong = dLong
        
    def convertLat(self):
        degrees = int(self.rawLat[:2])
        minutes = float(self.rawLat[2:])
        decimalDegrees = degrees + minutes / 60
        return decimalDegrees

    def convertLong(self):
        degrees = int(self.rawLong[:3])
        minutes = float(self.rawLong[3:])
        decimalDegrees = degrees + minutes / 60
        return decimalDegrees

    def timeToBinary(self):
        #use raw time cause its much easier
        hours = self.rawTime[:2]
        mins = self.rawTime[2:4]
        seconds = self.rawTime[4:6]
        totSecs = (int(hours) * 3600) + (int(mins) * 60) + int(seconds)
        return format(totSecs, '017b')

    def latToBinary(self):
        decimalDegrees = self.convertLat()
        latInt = int(abs(decimalDegrees * 100000))
        return format(latInt, '024b')

    def longToBinary(self):
        decimalDegrees = self.convertLong()
        longInt = int(abs(decimalDegrees * 100000))
        return format(longInt, '025b')
    
    def latDirBinary(self):
        if self.dLat == 'S':
            return format(1, '01b')
        else:
            return format(0, '01b')
        
    def longDirBinary(self):
        if self.dLong == 'W':
            return format(1, '01b')
        else:
            return format(0, '01b')

    def print(self):
        print(f"Time: {self.rawTime}, Lat: {self.convertLat()}, Lat Direction: {self.dLat}, Long: {self.convertLong()}, Long Direction: {self.dLong}")

    def printBinary(self):
        print(f"Time: {self.timeToBinary()}, Lat: {self.latToBinary()}, Lat Direction: {self.latDirBinary()}, Long: {self.longToBinary()}, Long Direction: {self.longDirBinary()}")


while True:
    time.sleep(0.1)
    raw_line = uart.readline()
    message, truth = filterLines(raw_line)
    if not truth:
        continue
    try:
        info = parseLine(message)
    except Exception as e:
        print(f"got error: {e}")
        continue
    info.print()
    info.printBinary()
