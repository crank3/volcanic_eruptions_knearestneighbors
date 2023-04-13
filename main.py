
import sys

import pandas as pd
import random
import numpy as np
import math
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import style


# user decided things
k = 5
known_rows = 600  # Number of known points of specific categories to find. Errors if this value is too large. 600
testing_rows = 100  # Number of unknown points of specific categories to find. 100
variables = ["Longitude", "Latitude"]  # ["variable 1", "variable 2", ...]    (variables that find neighbors)
determined_variable = "Type"  # name of the feature that the algorithm determines
all_groups = [["Submarine", 'cyan'], ["Shield", 'magenta'], ["Caldera", 'lime'], ["Volcanic field", 'red'], ["Pyroclastic cone", 'orange'], ["Lava dome", 'white'], ["Complex", 'blue'], ["Fissure vent", 'yellow'], ["Maar", 'green']]  # [["category', 'color'], ...]         (TBD categories)
# Stratovolcano is very common
# [["Submarine", 'cyan'], ["Shield", 'magenta'], ["Caldera", 'lime'], ["Volcanic field", 'red'], ["Pyroclastic cone", 'orange'], ["Lava dome", 'white'], ["Complex", 'blue'], ["Fissure vent", 'yellow'], ["Maar", 'green']]



# getting the data
data_file = (pd.read_csv("volcanic_eruptions.csv", header=0)).values.tolist()  # data_file = a 2D list of the csv file
header_row = ((pd.read_csv("volcanic_eruptions.csv", nrows=1)).columns).values.tolist()
possible_groups = [["Submarine", 0]]
for row in data_file:
    row[4] = row[4].replace('(s)', '')
    row[4] = row[4].replace('(es)', '')
    row[4] = row[4].replace('?', '')
    # print(row[4])

    in_possible_groups = False
    for group_i in possible_groups:
        if group_i[0] == row[4]:
            in_possible_groups = True
            group_i[1] += 1
    if not in_possible_groups:
        possible_groups.append([row[4], 1])

print(f'All Possible Groups: {possible_groups}\n')
# print(f'Header: {header_row}')


# creating an array with all of the group names in the same order as the array all_groups
all_group_names = []
for group_iiiii in all_groups:
    all_group_names.append(group_iiiii[0])
    print(group_iiiii)


# setting the plot background as a map
img = plt.imread("world_map.jpg")
fig, ax = plt.subplots()
ax.imshow(img, extent=(-183, 183, -67, 100))


def groupPoint(grouped_points_k, point_u, k):
    # grouped_points_k = the 2D array of known points
    # point_u = the unknown point that whose point must be decided
    # k = the number of nearest points to consider when deciding the group of point_u

    # all point objects must be in the following format:  [x position, y position, category]

    # calculating distances
    distance_and_group = []
    for point in grouped_points_k:

        euclidean_dist = math.sqrt(((point[0]-point_u[0])**2)+((point[1]-point_u[1])**2))

        distance_and_group.append([euclidean_dist, point[2]])

    distance_and_group = sorted(distance_and_group)
    k_nearest_points = distance_and_group[:k]

    # calculating the majority group and returning its name
    group_scores = []
    for group in all_groups:
        group_scores.append(0)

    for chosen_point in k_nearest_points:
        group_scores[all_group_names.index(chosen_point[1])] += 1

    return all_group_names[group_scores.index(max(group_scores))]


def main():


    # randomly choosing which points are known and which are unknown / putting them in separate 2D lists
    remaining_data = data_file
    known_points = []
    unknown_points = []
    while ((len(known_points) < known_rows) or (len(unknown_points) < testing_rows)) and (len(remaining_data) > 0):
        random_element = random.choice(remaining_data)
        random_row = remaining_data.index(random_element)

        transformed_random_element = [random_element[header_row.index(variables[0])],
                                      random_element[header_row.index(variables[1])],
                                      random_element[header_row.index(determined_variable)]]  # [x, y, category]

        # print(f'\nRow: {random_row}\nObject: {remaining_data[random_row]}\nknown_points length: {len(known_points)}\nunknown_points length: {len(unknown_points)}\nremaining points: {len(remaining_data)}')

        if len(remaining_data) == 1:
            print(f'\n*** NOT ENOUGH DATA ***\nknown_points length: {len(known_points)}\nunknown_points length: {len(unknown_points)}')

        remaining_data.pop(random_row)

        for group_name_i in all_group_names:
            if transformed_random_element[2] == group_name_i:
                if len(known_points) < known_rows:
                    known_points.append(transformed_random_element)
                    x = transformed_random_element[0]
                    y = transformed_random_element[1]
                    plt.plot(x, y, 'o', color=all_groups[all_group_names.index(transformed_random_element[2])][1], markersize=4)
                elif len(unknown_points) < testing_rows:
                    unknown_points.append(transformed_random_element)


    # running algorithm / measuring accuracy
    total_correct = 0
    for u_point_i in unknown_points:
        result = groupPoint(known_points, u_point_i, k)

        if result == u_point_i[2]:
            total_correct += 1

        x = u_point_i[0]
        y = u_point_i[1]
        plt.plot(x, y, 'x', color=all_groups[all_group_names.index(result)][1], markersize=8)

    print(f'\nPercent Accuracy: {(total_correct / testing_rows) * 100} %')
    print(f'Expected Accuracy if it were just guessing randomly: {100 / len(all_groups)} %')

    # plotting
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()


if __name__ == '__main__':
    main()
# :)
