
def latToBin(lat):
    latInt = int(abs(lat * 100000))
    return format(latInt, '024b')

def longToBin(long):
    longInt = int(abs(long * 100000))
    return format(longInt, '025b')

lat = float(input("Please enter Lat: "))

long = float(input("Please enter long: "))

print(f"Binary representation of Lattitude: {latToBin(lat)}" )
print(f"Binary representation of Longitude: {longToBin(long)}" )