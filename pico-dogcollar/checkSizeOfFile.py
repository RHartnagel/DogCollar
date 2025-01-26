import os

print("Files:", os.listdir())

file_name = "locations"
file_stats = os.stat(file_name)
file_size = file_stats[6]
print(f"File Size of '{file_name}': {file_size} bytes")