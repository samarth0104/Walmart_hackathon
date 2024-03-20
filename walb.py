import numpy as np
import csv
from math import radians, sin, cos, sqrt, atan2


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


# Define the path to the input CSV file
input_csv_file = "part_b_input_dataset_1.csv"

# Read data from the CSV file
data = []
with open(input_csv_file, newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

# Convert latitude and longitude strings to float
for item in data:
    item["lat"] = float(item["lat"])
    item["lng"] = float(item["lng"])

# Calculate the distance matrix between all pairs of locations
num_locations = len(data)
distance_matrix = np.zeros((num_locations, num_locations))
for i in range(num_locations):
    for j in range(num_locations):
        if i != j:
            distance_matrix[i][j] = haversine_distance(
                data[i]["lat"], data[i]["lng"], data[j]["lat"], data[j]["lng"]
            )


def nearest_neighbor(distance_matrix, capacity):
    num_locations = len(distance_matrix)
    routes = []

    # Initialize visited array to keep track of visited locations
    visited = [False] * num_locations

    # Iterate over each vehicle
    for vehicle in range(1, num_vehicles + 1):
        route = []
        current_location = 0  # Start from depot

        # Visit customers until capacity is reached or all customers are visited
        while len(route) < capacity and len(route) < num_locations - 1:
            # Find nearest unvisited customer location
            min_distance = float("inf")
            next_location = None
            for neighbor in range(1, num_locations):
                if (
                    not visited[neighbor]
                    and distance_matrix[current_location][neighbor] < min_distance
                ):
                    min_distance = distance_matrix[current_location][neighbor]
                    next_location = neighbor

            print("Current Location:", current_location)
            print("Next Location:", next_location)

            if next_location is None:
                print("Error: No more unvisited locations found!")
                break

            # Update current location and add next location to route
            current_location = next_location
            route.append(current_location)
            visited[current_location] = True

        # Add depot to complete the route
        route.append(0)
        routes.append(route)

    return routes


# Write delivery routes for each vehicle to the output dataset
def write_routes_to_csv(routes, output_csv_file):
    with open(input_csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "order_id",
                "lng",
                "lat",
                "depot_lat",
                "depot_lng",
                "vehicle_num",
                "dlvr_seq_num",
            ]
        )

        dlvr_seq_num = 1
        for vehicle_num, route in enumerate(routes, start=1):
            for i, location in enumerate(route[:-1]):
                order_id = data[location]["order_id"]
                lng = data[location]["lng"]
                lat = data[location]["lat"]
                depot_lat = data[0]["lat"]
                depot_lng = data[0]["lng"]
                writer.writerow(
                    [
                        order_id,
                        lng,
                        lat,
                        depot_lat,
                        depot_lng,
                        vehicle_num,
                        dlvr_seq_num,
                    ]
                )
                dlvr_seq_num += 1

    print("Delivery routes have been written to:", output_csv_file)


# Calculate total distance traveled across vehicles
def calculate_total_distance(routes, distance_matrix):
    total_distance = 0
    for route in routes:
        distance = 0
        for i in range(len(route) - 1):
            distance += distance_matrix[route[i]][route[i + 1]]
        total_distance += distance
    return total_distance


# Write total distance traveled across vehicles to a separate file
def write_total_distance_to_file(total_distance, input_distance_file):
    with open(input_distance_file, "w") as file:
        file.write(
            "Total distance traveled across vehicles: {} kms".format(total_distance)
        )

    print(
        "Total distance traveled across vehicles has been written to:",
        input_distance_file,
    )


# Provide high-level explanation and complexity details in the output details file
output_details_file = "part_b_details.txt"
with open(output_details_file, "w") as file:
    file.write("Vehicle Routing Algorithm using Nearest Neighbor\n")
    file.write("Time Complexity:\n")
    file.write(
        "- Nearest Neighbor Algorithm: O(n^2) where n is the number of customer locations.\n"
    )
    file.write(
        "- Writing Delivery Routes: O(n) where n is the number of customer locations.\n"
    )
    file.write(
        "- Calculating Total Distance: O(n) where n is the number of customer locations.\n"
    )
    file.write("Space Complexity:\n")
    file.write(
        "- Nearest Neighbor Algorithm: O(n^2) for storing the distance matrix.\n"
    )
    file.write("- Output Dataset: O(n) for storing the delivery routes.\n")
    file.write("- Total Distance File: O(1) for storing a single value.\n")

# Example usage
num_vehicles = 2
vehicle_capacity = 20
routes = nearest_neighbor(distance_matrix, vehicle_capacity)
write_routes_to_csv(routes, "part_b_output_dataset_1.csv")
total_distance = calculate_total_distance(routes, distance_matrix)
write_total_distance_to_file(total_distance, "part_b_routes_distance_travelled.csv")
