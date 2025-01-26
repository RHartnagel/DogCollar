with open("locations", 'rb') as file:
    while True:
        line = file.read(9)
        if not line:
            break
        
        binary_representation = ''.join(f'{byte:08b}' for byte in line)
        
        print(f"Raw Bytes: {line}")
        print(f"Binary Representation: {binary_representation}")
