import numpy as np
import csv
from math import radians, sin, cos, sqrt, atan2
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_local_search


# Define the Haversine distance function
def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers
    return distance


# Define the path to your CSV file
input_csv_file = "part_a_input_dataset_5.csv"

# Read data from CSV file
data = []
with open(input_csv_file, newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

array = []
for item in data:
    array.append([float(item["lng"]), float(item["lat"])])  # Convert string to float

# Calculate the Haversine distance matrix
num_points = len(array)
distance_matrix = np.zeros((num_points, num_points))
for i in range(num_points):
    for j in range(num_points):
        if i != j:
            distance_matrix[i][j] = haversine_distance(
                array[i][1], array[i][0], array[j][1], array[j][0]
            )

# Solve TSP using dynamic programming
permutation, distance = solve_tsp_local_search(distance_matrix)

# Update data with dlvr_seq_num
for i, item in enumerate(data):
    item["dlvr_seq_num"] = permutation[i] + 1  # Add 1 to start from 1

# Write updated data to CSV file
fieldnames = data[0].keys()
with open(input_csv_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
print(distance)
